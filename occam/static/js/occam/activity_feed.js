var occam = angular.module("occam", []);

occam.controller('ActivityFeed', function ($scope, $location, $http) {

    $scope.init = function(chunkSize) {
        $scope.chunkSize = chunkSize || 100;
        $scope.reset();
    };

    $scope.$watch(function() { return $location.search(); }, function() {
        $scope.search = $location.search().filter || "";
    });

    $scope.$watch('search', function(filter) {
        $location.search('filter', filter);
    });

    $scope.$watch(function($scope) { return $scope.selectedNode; }, function() {
        if ($scope.selectedNode) {
            $scope.reset();
        }
    });

    $scope.reset = function() {
        $("#activityFeedEntries").addClass("darken");
        $("#loadButton").prop('disabled', true);
        $("#refreshButton").prop('disabled', true);
        var seedData = window.seed_data;
        window.seed_data = {};
        $scope.omittedKeys = ['event', 'timestamp'];
        $scope.nodes = seedData.nodes || [];
        $scope.entries = seedData.entries || [];

        $scope.first_entry = seedData.entry_start || 0;
        $scope.last_entry = seedData.entry_end || -1;
        $scope.max_entry = seedData.max_entry || 0;

        if ($scope.entries.length === 0) {
            $scope.loadMore();
        } else {
            $("#activityFeedEntries").removeClass("darken");
            $("#loadButton").prop('disabled', false);
            $("#refreshButton").prop('disabled', false);
        }
    };

    $scope.loadMore = function() {
        $("#loadButton").prop('disabled', true);
        var request_start = $scope.last_entry + 1;
        var request_end = request_start + ($scope.chunkSize - 1);
        var basePath = "/activity";
        if ($scope.selectedServer && $scope.selectedNode) {
            basePath = "/activity/" + $scope.selectedServer + "/" + $scope.selectedNode;
        }
        // TODO: this is gross.
        var url = basePath + '?start=' + request_start + '&end=' + request_end;
        $http.get(url).success(function(data) {
            $scope.last_entry = parseInt(data.end, 10);
            $scope.max_entry = parseInt(data.max_end, 10);

            $.extend(true, $scope.nodes, data.nodes);
            $scope.entries.push.apply($scope.entries, data.entries);
            $("#loadButton").prop('disabled', false);
            $("#refreshButton").prop('disabled', false);
            $("#activityFeedEntries").removeClass("darken");
        });
    };
});
