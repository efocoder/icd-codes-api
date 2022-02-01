from django_seed import Seed

from codes.models import IcdCodeRecord
from users.models import User, Category


class Code:
    def __init__(self, code: str = None, category: str = None, description: str = None, prefix: str = None):
        self.code = code
        self.category_code = category
        self.description = description
        self.prefix = prefix


seeder = Seed.seeder()


def seed_user():
    seeder.add_entity(User, 1, {
        'email': 'clem.clem@gmail.com',
        'password': 'password'
    })


# def seed_code_edition():
#     codes = ['ICD-6', 'ICD-7', 'ICD-8', 'ICD-9', 'ICD-10']
#     for code in codes:
#         seeder.add_entity(CodeEdition, 1, {
#             'edition_code': code
#         })


def seed_category():
    users = User.objects.filter(status='ACTIVE')
    categories = {
        "A00": "Cholera",
        "A01": "Typhoid and paratyphoid fevers",
        'A010': 'Typhoid fever',
        "A011": "Paratyphoid fever A",
        "A012": "Paratyphoid fever B"
    }

    for category in categories:
        for user in users:
            seeder.add_entity(Category, 1, {
                'created_by': user,
                'category_code': category,
                'description': categories[category]
            })

        # print(users)


def seed_codes():
    users = User.objects.filter(status='ACTIVE')
    categories = Category.objects.filter(status='ACTIVE')
    code_list = [
        Code("A000", "A00", "Cholera due to Vibrio cholerae 01, biovar cholerae", '0'),
        Code("A001", "A00", "Cholera due to Vibrio cholerae 01, biovar eltor", '1'),
        Code("A009", "A00", "Cholera, unspecified", '9'),
        Code("A0100", "A010", "Typhoid fever, unspecified", '0'),
        Code("A010", "A0101", "Typhoid meningitis", '1'),
    ]
    for code_obj in code_list:
        for user in users:
            for _ in categories:
                cat = Category.objects.filter(status='ACTIVE', category_code__exact=code_obj.category_code).first()
                print(cat)
                # print(code_obj.category_code)
                if cat:
                    seeder.add_entity(IcdCodeRecord, 1, {
                        "icd_code": code_obj.code,
                        "icd_code_prefix": code_obj.prefix,
                        "description": code_obj.description,
                        "created_by": user,
                        "category": cat
                    })
                break


seed_user()
# Execute the first seed to create user, so we can load user while creating category
print("running user seed")
print("###############################")
seeder.execute()

print("running user seed done")
# Execute the category seed
print("running category seed")
print("###############################")
seed_category()
seeder.execute()
print("running category seed done")
seed_codes()
seeder.execute()
