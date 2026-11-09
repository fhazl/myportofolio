import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience, Project


class MainTest(TestCase):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_removed_verb_urls_return_404(self):
        for path in ("/education/add/", "/experience/add/", "/projects/add/"):
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_page_shells_render_and_set_csrf_cookie(self):
        pages = {
            "main:show_experience": "experience.html",
            "main:show_education": "education.html",
            "main:show_projects": "project.html",
        }
        for name, template in pages.items():
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
            self.assertContains(response, 'id="grid"')
            self.assertIn("csrftoken", response.cookies)


class ModelTest(TestCase):
    def test_experience_model(self):
        experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
            started_at=datetime.date(2025, 8, 1),
        )
        self.assertEqual(str(experience), "PBP Teaching Assistant")
        self.assertEqual(experience.category, "part-time")
        self.assertTrue(experience.is_ongoing)

    def test_completed_experience(self):
        experience = Experience.objects.create(
            title="Intern", description="Work", category="internship",
            started_at=datetime.date(2025, 1, 1),
            ended_at=datetime.date(2025, 6, 1),
        )
        self.assertFalse(experience.is_ongoing)

    def test_education_model(self):
        education = Education.objects.create(
            degree="Bachelor", institution="Universitas Indonesia",
            field_of_study="Computer Science",
            started_at=datetime.date(2024, 8, 1),
        )
        self.assertEqual(
            str(education),
            "Bachelor in Computer Science - Universitas Indonesia",
        )
        self.assertTrue(education.is_ongoing)


class RoleSetupMixin:
    """Creates the four roles from Tugas 4 and an Education record."""

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.editor = User.objects.create_user("editor", password="pass12345")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.user = User.objects.create_user("regular", password="pass12345")

        self.education = Education.objects.create(
            degree="Bachelor", institution="Universitas Indonesia",
            field_of_study="Computer Science", description="Original",
            started_at=datetime.date(2024, 8, 1),
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse(
            "api:education-detail", kwargs={"education_id": self.education.id},
        )
        self.star_url = reverse(
            "api:education-star", kwargs={"education_id": self.education.id},
        )
        self.payload = {
            "degree": "Master", "institution": "ITB",
            "field_of_study": "Informatics", "description": "New",
            "started_at": "2026-08-01",
        }


class EducationReadTest(RoleSetupMixin, APITestCase):
    def test_visitor_can_list_and_retrieve(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["degree"], "Bachelor")

    def test_search_filters_by_degree(self):
        Education.objects.create(
            degree="Diploma", institution="X", field_of_study="Y",
            started_at=datetime.date(2020, 1, 1),
        )
        response = self.client.get(self.list_url, {"degree": "dipl"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["degree"], "Diploma")

    def test_unknown_id_returns_404(self):
        url = reverse(
            "api:education-detail",
            kwargs={"education_id": "00000000-0000-0000-0000-000000000000"},
        )
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_response_hides_sensitive_account_data(self):
        self.education.starred_by.add(self.user)
        response = self.client.get(self.detail_url)
        body = str(response.data)
        self.assertNotIn("password", body)
        self.assertNotIn("email", body)
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "regular")


class EducationPermissionTest(RoleSetupMixin, APITestCase):
    def test_visitor_cannot_write(self):
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(
            self.client.patch(self.detail_url, {"degree": "Hacked"}, format="json").status_code, 403,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Bachelor")

    def test_regular_user_cannot_write(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(
            self.client.patch(self.detail_url, {"degree": "Hacked"}, format="json").status_code, 403,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Bachelor")

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"degree": "Edited"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Edited")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Master")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.count(), 2)

        response = self.client.patch(self.detail_url, {"degree": "Owner Edit"}, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())


class EducationValidationTest(RoleSetupMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.owner)

    def test_html_tags_are_stripped(self):
        data = {**self.payload, "degree": "<b>Master</b>", "description": "<script>x</script>Hi"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        created = Education.objects.get(pk=response.data["id"])
        self.assertEqual(created.degree, "Master")
        self.assertNotIn("<", created.description)

    def test_tag_only_degree_is_rejected(self):
        data = {**self.payload, "degree": "<b></b>"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("degree", response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_missing_required_field_is_rejected(self):
        data = {k: v for k, v in self.payload.items() if k != "institution"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.data)

    def test_computed_fields_are_read_only(self):
        data = {**self.payload, "star_count": 99, "is_starred": True, "id": "x"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])


class EducationStarTest(RoleSetupMixin, APITestCase):
    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_user_can_star_and_unstar(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertIn(self.user, self.education.starred_by.all())

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_star_uses_request_user_only(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
        self.assertEqual(list(self.education.starred_by.all()), [self.user])

    def test_star_unknown_id_returns_404(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "api:education-star",
            kwargs={"education_id": "00000000-0000-0000-0000-000000000000"},
        )
        self.assertEqual(self.client.post(url).status_code, 404)


class EducationCsrfTest(RoleSetupMixin, APITestCase):
    def test_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="pass12345"))

        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_write_with_csrf_token_is_accepted(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="pass12345")
        client.get(reverse("main:show_education"))
        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.count(), 2)


class ExperienceApiTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.editor = User.objects.create_user("editor", password="pass12345")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.experience = Experience.objects.create(
            category="part-time", title="PBP Teaching Assistant",
            description="Help students.", started_at=datetime.date(2025, 8, 1),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", kwargs={"experience_id": self.experience.id},
        )
        self.star_url = reverse(
            "api:experience-star", kwargs={"experience_id": self.experience.id},
        )
        self.payload = {
            "category": "internship", "title": "Backend Intern",
            "description": "APIs", "started_at": "2026-01-01",
        }

    def test_visitor_can_read_and_search(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        response = self.client.get(self.list_url, {"title": "teaching"})
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["is_ongoing"])

    def test_visitor_cannot_write(self):
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_patch_only(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_create_and_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 204)
        self.assertEqual(Experience.objects.count(), 1)

    def test_tag_only_title_is_rejected(self):
        self.client.force_authenticate(self.owner)
        data = {**self.payload, "title": "<i></i>"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Experience.objects.count(), 1)

    def test_star_requires_login(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(self.editor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.data["star_count"], 1)


class MeEndpointTest(APITestCase):
    def setUp(self):
        self.url = reverse("api:me")
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.editor = User.objects.create_user("editor", password="pass12345")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.user = User.objects.create_user("regular", password="pass12345")

    def test_visitor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "is_authenticated": False, "is_superuser": False,
            "is_editor": False, "username": None,
        })

    def test_regular_user(self):
        self.client.force_authenticate(self.user)
        data = self.client.get(self.url).data
        self.assertTrue(data["is_authenticated"])
        self.assertFalse(data["is_superuser"])
        self.assertFalse(data["is_editor"])

    def test_editor(self):
        self.client.force_authenticate(self.editor)
        self.assertTrue(self.client.get(self.url).data["is_editor"])

    def test_owner(self):
        self.client.force_authenticate(self.owner)
        self.assertTrue(self.client.get(self.url).data["is_superuser"])

    def test_response_has_no_sensitive_fields(self):
        self.client.force_authenticate(self.owner)
        self.assertEqual(
            set(self.client.get(self.url).data),
            {"is_authenticated", "is_superuser", "is_editor", "username"},
        )

    def test_me_is_read_only(self):
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.post(self.url).status_code, 405)