import requests, datetime


class IikoCardAPI:
    """ Класс для работы с API iiko"""

    def __init__(self, apiLogin, timeout=180):
        self.apiLogin = apiLogin
        self.timeout = timeout
        self.apiURL = "https://api-ru.iiko.services/api/1/"
        self.session = requests.Session()
        self.organization_id = None
        self.__token_date = datetime.timedelta(days=1)  # The standard token lifetime is 1 hour.
        self.token = self.set_token()

    def __check_token(self) -> bool:
        ...

    def set_token(self) -> str:
        """Запрашивает и устанавливает сессию с токеном для класса
        :return: str - токен
        """
        time_delta = (datetime.datetime.now() - self.__token_date)
        if not hasattr(self, 'token') or not self.token or (time_delta > datetime.timedelta(hours=1)):
            try:
                self.token = \
                    self.session.post(f"{self.apiURL}access_token", json={"apiLogin": self.apiLogin},
                                      timeout=self.timeout).json()[
                        'token']
                self.session.headers['Authorization'] = f'Bearer {self.token}'
                self.__token_date = datetime.datetime.now()
                print('Токен установлен! ', time_delta)
            except requests.exceptions.ConnectTimeout:
                print(f"Не удалось получить токен для \n{self.apiLogin}")
            except KeyError:
                print("Не корректный запрос(логин API?).")
        return self.token

    def organizations(self, includeDisabled: bool = False):
        """
         Получение сведений об организациях
        :param includeDisabled (optional): False - включать в ответ отключенные организации
        :return: iiko .json response
        """
        self.set_token()
        result = None
        try:
            result = self.session.post(f"{self.apiURL}organizations", json={"includeDisabled": includeDisabled},
                                       timeout=self.timeout)
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список организаций.")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def set_organization(self, organizationId: str):
        self.organization_id = organizationId

    def loyalty_programs(self, organizationId: str = None):
        """ Получение сведений о программах лояльности по ID организации
            :return: iiko .json response"""
        self.set_token()
        result = None
        data = {"organizationId": organizationId if organizationId else self.organization_id}
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/program", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список действующих программ")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_customer_by_id(self, userId: str, organizationId: str = None):
        """
        Получить информацию о пользователе по ID
        :param userId: ID пользователя
        :param organizationId: ID организации (необязательно)
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = {
            "id": userId,
            "type": "id",
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/info", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_customer_by_phone(self, userPhone: str, organizationId: str = None):
        """
        Получить информацию о пользователе по номеру телефона
        :param userPhone: Телефон пользователя
        :param organizationId: ID организации (необязательно)
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = {
            "phone": userPhone,
            "type": "phone",
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/info", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_customer_by_card(self, cardNumber: str, organizationId: str = None):
        """
        Получить информацию о пользователе по номеру карточки
        :param cardNumber: Номер карточки
        :param organizationId: ID организации (необязательно)
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = {
            "cardNumber": cardNumber,
            "type": "cardNumber",
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/info", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_customer_by_cardTrack(self, cardTrack: str, organizationId: str = None):
        """
        Получить информацию о пользователе по номеру Трека карточки
        :param cardTrack: Трек карточки пользователя
        :param organizationId: ID организации (необязательно)
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = {
            "cardTrack": cardTrack,
            "type": "cardTrack",
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/info", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def create_or_update_customer(self, payload: dict):
        """
        Изменить или создать пользователя
        :param payload: json dict
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = payload
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/create_or_update", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_add_card(self, customerId: str, cardTrack: str, cardNumber: str, organizationId: str = None):
        """
        Добавить карту пользователя
        :param customerId:
        :param cardTrack:
        :param cardNumber:
        :param organizationId: (optional)
        :return:
        """
        self.set_token()
        result = None
        data = {
            "customerId": customerId,
            "cardTrack": cardTrack,
            "cardNumber": cardNumber,
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/card/add", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_delete_card(self, customerId: str, cardTrack: str, organizationId: str = None):
        """
        Удалить карту пользователя
        :param customerId:
        :param cardTrack:
        :param organizationId: (optional)
        :return:
        """
        self.set_token()
        result = None
        data = {
            "customerId": customerId,
            "cardTrack": cardTrack,
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/card/remove", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить информацию о пользователе")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_categories(self, organizationId: str = None):
        """ Получение сведений о категориях лояльности, доступных для организации.
            :return: iiko .json response"""
        self.set_token()
        result = None
        data = {"organizationId": organizationId if organizationId else self.organization_id}
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer_category", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список доступных категорий")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_select_category(self, customerId: str, categoryId: str, organizationId: str = None):
        """ Добавить категорию пользователю
        :param customerId: ID пользователя
        :param categoryId: ID категории
        :param organizationId: (optional)"""
        self.set_token()
        result = None
        data = {
            "customerId": customerId,
            "categoryId": categoryId,
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer_category/add", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось добавить категорию пользователю")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_remove_category(self, customerId: str, categoryId: str, organizationId: str = None):
        """ Удалить категорию пользователю
        :param customerId: ID пользователя
        :param categoryId: ID категории
        :param organizationId: (optional)"""
        self.set_token()
        result = None
        data = {
            "customerId": customerId,
            "categoryId": categoryId,
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer_category/remove", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось удалить категорию пользователю")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def loyalty_select_program(self, customerId: str, programId: str, organizationId: str = None):
        """ Добавить категорию пользователю
        :param customerId: ID пользователя
        :param programId: ID программы
        :param organizationId: (optional)"""
        self.set_token()
        result = None
        data = {
            "customerId": customerId,
            "programId": programId,
            "organizationId": organizationId if organizationId else self.organization_id
        }
        try:
            result = self.session.post(f"{self.apiURL}loyalty/iiko/customer/program/add", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось добавить пользователя в программу лояльности")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_service_organization(self, organizationId: str = None):
        """ Получение сведений об обслуживаемых организациях
            :return: iiko .json response"""
        self.set_token()
        result = None
        data = {"organizationIds": [organizationId if organizationId else self.organization_id]}
        try:
            result = self.session.post(f"{self.apiURL}reserve/available_organizations", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список доступных к обслуживанию организаций")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

    def get_terminal_groups(self, organizationId: str = None, includeDisabled: bool = False):
        """
        Получение сведений о терминалах организации
        :param organizationId(optional): None - если не установлено, используется по умолчанию
        :param includeDisabled(optional): False - включая отключенные
        :return: iiko .json response
        """
        self.set_token()
        result = None
        data = {"organizationIds": [organizationId if organizationId else self.organization_id],
                "includeDisabled": includeDisabled
                }
        try:
            result = self.session.post(f"{self.apiURL}reserve/available_terminal_groups", json=data, timeout=self.timeout, )
            if result.status_code == 401:
                raise ZeroDivisionError
            result = result.json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список доступных к обслуживанию организаций")
        except ZeroDivisionError:
            self.token = None
            print("Not authorized")
        return result

