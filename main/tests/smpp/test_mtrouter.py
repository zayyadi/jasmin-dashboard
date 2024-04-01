# Generated by CodiumAI

# Dependencies:
# pip install pytest-mock
import pytest


class Test_List:
    # Tests that the method returns a dictionary with 'mointerceptor' key and a list of dictionaries with 'type' and 'script' keys when mointerceptor_result has length greater than or equal to 3
    def test_happy_path(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method
        telnet_mock.sendline.return_value = None

        # Mock the expect method
        telnet_mock.expect.return_value = None

        # Mock the split_cols function
        mocker.patch(
            "main.core.tools.split_cols",
            return_value=[["type1", "script1"], ["type2", "script2"]],
        )

        # Call the _list method
        result = self.obj._list()

        # Assert the result
        assert result == {
            "mointerceptor": [
                {"type": "type1", "script": "script1"},
                {"type": "type2", "script": "script2"},
            ]
        }

    # Tests that the method returns a dictionary with 'morouters' and 'users' keys and empty lists when mointerceptor_result has length less than 3
    def test_empty_result(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method
        telnet_mock.sendline.return_value = None

        # Mock the expect method
        telnet_mock.expect.return_value = None

        # Call the _list method
        result = self.obj._list()

        # Assert the result
        assert result == {"morouters": [], "users": []}

    # Tests that the method returns a dictionary with 'morouters' and 'users' keys and empty lists when mointerceptor_result is empty
    def test_empty_mointerceptor_result(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method
        telnet_mock.sendline.return_value = None

        # Mock the expect method
        telnet_mock.expect.return_value = None

        # Call the _list method
        result = self.obj._list()

        # Assert the result
        assert result == {"morouters": [], "users": []}

    # Tests that the method raises an exception when telnet.sendline raises an exception
    def test_telnet_sendline_exception(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method to raise an exception
        telnet_mock.sendline.side_effect = Exception("Sendline exception")

        # Call the _list method and expect an exception
        with pytest.raises(Exception, match="Sendline exception"):
            self.obj._list()

    # Tests that the method raises an exception when telnet.expect raises an exception
    def test_telnet_expect_exception(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method
        telnet_mock.sendline.return_value = None

        # Mock the expect method to raise an exception
        telnet_mock.expect.side_effect = Exception("Expect exception")

        # Call the _list method and expect an exception
        with pytest.raises(Exception, match="Expect exception"):
            self.obj._list()

    # Tests other cases not covered by the previous tests
    def test_other_cases(self, mocker):
        # Mock the telnet object
        telnet_mock = mocker.Mock()
        self.obj.telnet = telnet_mock

        # Mock the sendline method
        telnet_mock.sendline.return_value = None

        # Mock the expect method
        telnet_mock.expect.return_value = None

        # Mock the split_cols function
        mocker.patch(
            "main.core.tools.split_cols",
            return_value=[["type1", "script1"], ["type2", "script2"]],
        )

        # Call the _list method
        result = self.obj._list()

        # Assert the result
        assert result == {
            "mointerceptor": [
                {"type": "type1", "script": "script1"},
                {"type": "type2", "script": "script2"},
            ]
        }