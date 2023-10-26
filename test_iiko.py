import unittest
from iiko import IikoCardAPI
from config import apiLogin
from icecream import ic


class TestIikoAPI_1(unittest.TestCase):
    api1 = IikoCardAPI(apiLogin)  # регистрация класса который будет использован в тестах
    token = api1.set_token()  # получение токена
    organizationid = api1.organizations()['organizations'][0]['id']  # выбор организации с которой будем работать
    api1.set_organization(organizationid)  # установка организации по умолчанию в классе для тестов

    def test_getToken(self) -> None:
        """ Проверка выдачи токена"""
        token = self.token
        self.assertIsNotNone(token)

    def test_organizations(self) -> None:
        """ Проверка выдачи организации"""
        self.assertEqual(self.organizationid, '1131645e-f44f-4766-8ce5-df84300c15a1')

    def test_loyalty_prg(self) -> None:
        """ Проверка выдачи программ лояльности"""
        print(self.api1.organization_id)
        lp = self.api1.loyalty_programs()
        ic(lp)
        self.assertIsNotNone(lp['Programs'])

    def test_get_customer_by_phone(self) -> None:
        """ Проверка выдачи информации о клиенте по номеру телефона"""
        info = self.api1.get_customer_by_phone("+70001112233")
        ic(info)
        self.assertEqual(info['name'], 'Виктор')

    def test_update_customer(self) -> None:
        """ Изменение информации о клиенте"""
        payload = {
            "phone": "+70001112233",
            "email": "test01@test.ru",
            "organizationId": self.organizationid
        }
        info = self.api1.create_or_update_customer(payload)
        ic(info)
        self.assertEqual(info['id'], '01330000-6bec-ac1f-d430-08db9a223fdd')

    def test_create_customer(self) -> None:
        """ Создание клиента"""
        payload = {
            "phone": "+70003332211",
            "organizationId": self.organizationid
        }
        info = self.api1.create_or_update_customer(payload)  # 'id': '03650000-6bec-ac1f-df89-08db9e28d696'
        ic(info)
        self.assertIsNotNone(info['id'])

    def test_add_card(self) -> None:
        """ Добавление карты"""
        info = self.api1.loyalty_add_card("01330000-6bec-ac1f-d430-08db9a223fdd", "44=333222111", "444333222111")
        ic(info)
        self.assertIsNotNone(info)

    def test_get_customer_by_card(self) -> None:
        """ Проверка выдачи информации о клиенте по номеру созданной карты"""
        info = self.api1.get_customer_by_card("444333222111")
        ic(info)
        self.assertEqual(info['name'], 'Виктор')

    def test_get_customer_by_cardTrack(self) -> None:
        """ Проверка выдачи информации о клиенте по треку созданной карты"""
        info = self.api1.get_customer_by_cardTrack("44=333222111")
        ic(info)
        self.assertEqual(info['name'], 'Виктор')

    def test_del_card(self) -> None:
        """ Удаление созданной карты"""
        info = self.api1.loyalty_delete_card("01330000-6bec-ac1f-d430-08db9a223fdd", "444333222111")
        ic(info)
        self.assertIsNotNone(info)

    def test_get_categories(self) -> None:
        """ Проверка выдачи категорий программы лояльности"""
        lc = self.api1.loyalty_categories()
        ic(lc)
        self.assertIsNotNone(lc['guestCategories'])

    def test_add_cat(self) -> None:
        """ Добавление категории"""
        info = self.api1.loyalty_select_category("01330000-6bec-ac1f-d430-08db9a223fdd",
                                                 "4ddc84ca-3efb-4fea-8efd-f45b4afb4e29")
        ic(info)
        result = self.api1.get_customer_by_id("01330000-6bec-ac1f-d430-08db9a223fdd")
        ic(result)
        self.assertEqual(result['categories'][0]['id'], "4ddc84ca-3efb-4fea-8efd-f45b4afb4e29")

    def test_del_cat(self) -> None:
        """ Удаление категории"""
        info = self.api1.loyalty_remove_category("01330000-6bec-ac1f-d430-08db9a223fdd",
                                                 "4ddc84ca-3efb-4fea-8efd-f45b4afb4e29")
        ic(info)
        result = self.api1.get_customer_by_id("01330000-6bec-ac1f-d430-08db9a223fdd")
        ic(result)
        self.assertListEqual(result['categories'], [])

    def test_create_cust_id(self):
        """ Создание клиента по треку"""
        payload = {
            "cardTrack": "80=3333",
            "organizationId": self.organizationid
        }
        info = self.api1.create_or_update_customer(payload)
        ic(info)
        self.assertIsNotNone(info['id'])  # 'id': '01330000-6bec-ac1f-ca14-08dbb5a409bd'

    def test_get_cust_by_cardTrack(self) -> None:
        """ Проверка выдачи информации о клиенте по треку созданной карты"""
        info = self.api1.get_customer_by_cardTrack("80=3333")
        ic(info)
        self.assertEqual(info['phone'], '+70000000005')
