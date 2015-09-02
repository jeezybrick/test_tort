/* Angular */

var testApp = angular.module('testApp', []);
//Контроллер для регистрации пользователя
testApp.controller('registrationCtrl', function ($scope, $http) {
  //$scope.login = 'jeezy';
    $http.get('/users/login_list').success(function (data) {
        $scope.data = data;
        $scope.login = '';
        $scope.loginExist = false;

        /*
         Функция проверки вводимого логина в JSON ,который пришел с БД.
         Выполняется при каждом вводе пользователя
         */
        $scope.check = function () {
            $scope.lol = data.filter(
                function (data) {
                    return data.login == $scope.login;
                }
            );

            if($scope.lol.length > 0 ){
                $scope.loginExist = true;
            }else{
                $scope.loginExist = false;
            }

        }
    });
});

testApp.controller('loginCtrl', function ($scope, $http) {
//
});
/*End Angular */