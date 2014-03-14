$( document ).ready(function() {
    $(document).on('click', 'dt > a.toggle', function(event) {
        var caret = $(this).children("span.caret");
        var valueBox = $(this).parent("dt").siblings("dd");
        var content = valueBox.children("");
        content.toggleClass("hidden");
        content.toggleClass("show");
        caret.toggleClass("caret-right");
        event.stopPropagation();
    });
});

var occam = angular.module("occam") || angular.module("occam", []);

occam.config(function($locationProvider) {
    $locationProvider.html5Mode(true);
});

occam.controller('NodeList', function ($scope, $location, $http) {
    $scope.nodes = window.seed_data.nodes || undefined;
    $scope.selectedNode = window.seed_data.start_node || undefined;
    $scope.selectedServer = window.seed_data.start_server || undefined;

    $scope.selectedNodeInfo = undefined;

    $scope.nodeOmittedKeys = ['log', 'policy', 'tags'];

    $scope.$watch(function() { return $location.path(); }, function() {
        var bits = $location.path().split("/");
        if (bits.length == 4) {
            $scope.selectedServer = bits[2];
            $scope.selectedNode = bits[3];
        } else {
            $scope.selectedServer = undefined;
            $scope.selectedNode = undefined;
        }
    });

    $scope.$watch(function($scope) { return $scope.selectedNode; }, function() {
        if ($scope.selectedServer && $scope.selectedNode) {
            $scope.selectedNodeInfo = $scope.nodes[$scope.selectedServer][$scope.selectedNode];
        } else {
            $scope.selectedNodeInfo = undefined;
        }
    });

    $scope.showNode = function(server, node) {
        $scope.selectedNode = $scope.nodes[server][node];
        $scope.selectedServer = server;
        $location.path("/nodes/" + node.name);
    };

    $scope.toggleSection = function(server) {
        var listKey = "#nodeList-" + server;
        var nodeList = $(listKey);
        var caret = nodeList.prev("div").children("a").children("span.caret");
        nodeList.toggle(0, function() {
            caret.toggleClass("caret-right");
        });
    };

    // This is like, the worst
    $scope.valueType = function(v) {
        if (angular.isObject(v)) {
            return "object";
        } else if (!isNaN(new Date(v).getMonth())) {
            return "date";
        } else {
            return "simple";
        }
    };
    $scope.isObject = function(v) {
        return angular.isObject(v);
    };
});

occam.filter('orderObjectByString', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
        a_val = a[field] || undefined;
        b_val = b[field] || undefined;
        if (!a_val && !b_val) { return 0; }
        else if (!a_val) { return 1; }
        else if (!b_val) { return -1; }
        else { return (a_val.localeCompare(b_val)); }
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});
