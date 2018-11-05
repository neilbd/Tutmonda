var app = angular.module('tutApp', ['ngRoute']);

app.controller('Controller', ['$scope', '$http', function($scope, $http){
	console.log("CONTROLLER EXECUTING");

	$http.get("/spiders", {'Accept': 'application/json', 'Access-Control-Allow-Origin': '*'}).then(function(response){
		
		console.log("SUCCESS");

		var data = angular.fromJson(response.data);
		console.log(data);
		$scope.news_col_one = [];
		$scope.news_col_two = [];

		console.log(typeof data);

		for(var i = 0; i < data.length; i++){

			if(data[i]['assigned_column']){

				if(data[i]["assigned_column"] === 1){
					console.log(data[i]);
					$scope.news_col_one.push(data[i]);				
				}else{
					console.log(data[i]);
					$scope.news_col_two.push(data[i]);
				}

			}
						
		}

		console.log($scope.news_col_one);
		console.log($scope.news_col_two);

	}, function(response){

		console.log("FAILED");
		console.log(response);

	});

}]);

app.config(function ($routeProvider) {
	console.log("EXECUTING ROUTEs");
	$routeProvider.when('/', {
		templateUrl: 'index.html',
		controller: 'Controller'
	}).otherwise({
		redirectTo: '/'
	});
});


