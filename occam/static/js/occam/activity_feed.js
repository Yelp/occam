var occam = angular.module("occam", []);

occam.controller('ActivityFeed', function ($scope) {
    $scope.omittedKeys = ['event', 'timestamp'];
    $scope.nodes = window.seed_data.nodes || [];
    $scope.entries = window.seed_data.entries || [];
});
