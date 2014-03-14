var collectionViewConfig = {
    "nodes": {
        "prioritizedKeys": ['policy', 'tags'],
        "omittedKeys": ['log']
    }
};

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

occam.controller('CollectionList', function ($scope, $location, $http) {
    $scope.init = function(collectionType) {
        var config = collectionViewConfig[collectionType] || {};
        console.log(config);
        $scope.prioritizedKeys = config.prioritizedKeys || [];
        $scope.omittedKeys = config.omittedKeys || [];
        $scope.omittedKeys = $scope.omittedKeys + $scope.prioritizedKeys;
    };

    $scope.items = window.seed_data.items || undefined;
    $scope.selectedItem = window.seed_data.start_item || undefined;
    $scope.selectedServer = window.seed_data.start_server || undefined;

    $scope.selectedItemInfo = undefined;

    $scope.$watch(function() { return $location.path(); }, function() {
        var bits = $location.path().split("/");
        if (bits.length == 4) {
            $scope.selectedServer = bits[2];
            $scope.selectedItem = bits[3];
        } else {
            $scope.selectedServer = undefined;
            $scope.selectedItem = undefined;
        }
    });

    $scope.$watch(function($scope) { return $scope.selectedItem; }, function() {
        if ($scope.selectedServer && $scope.selectedItem) {
            $scope.selectedItemInfo = $scope.items[$scope.selectedServer][$scope.selectedItem];
        } else {
            $scope.selectedItemInfo = undefined;
        }
    });

    $scope.toggleSection = function(server) {
        var listKey = "#itemList-" + server;
        var itemList = $(listKey);
        var caret = itemList.prev("div").children("a").children("span.caret");
        itemList.toggle(0, function() {
            caret.toggleClass("caret-right");
        });
    };

    // This is like, the worst
    $scope.valueType = function(v) {
        if (angular.isObject(v)) {
            if (v.name && v.id && v.spec) {
                return "reference";
            } else {
                return "object";
            }
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
