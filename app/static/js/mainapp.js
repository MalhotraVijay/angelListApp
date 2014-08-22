//var AngelAppModel = function () {
//
//    this.buildTemplate = function (jobObj, locationTag) {
//
//        var template = '<div class="singleJob-row card">' +
//            '<div class="jobTitle col-md-3">' + jobObj.title + '</div>' +
//            '<div class="jobStartupName col-md-2">' + jobObj.startup.name + '</div>' +
//            '<div class="jobDate col-md-2"> ' + jobObj.created_at + '</div>' +
//            '<div class="jobUrl col-md-3"> ' + jobObj.angellist_url + '</div>' +
//            '<div class="jobLocation col-md-2"> ' + locationTag + '</div>' +
//            '<div class="else">' + '.' + '</div>' +
//            '</div>'
//        $('#allJobsDetail').append(template);
//    };
//
//
//    this.displayAllJobsByPage = function (pageid) {
//        payloadJson = JSON.parse(jobsArr[pageid - 1].payload);
//
//        payloadJson.jobs.forEach(function (jobObj, index) {
//            var locationTag = '';
//            tags = jobObj.tags;
//            tags.forEach(function (tag, index) {
//                if (tag.tag_type == "LocationTag") {
//                    locationTag = tag.name;
//                    locationArr.push(tag.name);
//
//                    var dict = {};
//                    dict[tag.name] = jobObj.id
//                    locationDict.push(dict);
//                    jobDetailsDict[jobObj.id] = jobObj;
//                }
//            });
//
//            //console.log(index);
//
//            ag.buildTemplate(jobObj, locationTag)
//
//
//        });
//    };
//
//    this.displayAllJobsByLocation = function (location) {
//        payloadJson = JSON.parse(jobsArr[0].payload);
//
//        var jobsToshow = [];
//
//        locationDict.forEach(function (dictObj, index) {
//            //console.log(dictObj[location]);
//
//            if (dictObj[location] && dictObj[location] !== 'undefined') {
//                jobsToshow.push(dictObj[location]);
//                this.displayAllJobsByJobId(dictObj[location], location);
//
//            }
//        });
//
//    };
//
//    this.displayAllJobsByJobId = function (jobId, location) {
//
//        console.log(jobDetailsDict[jobId]);
//        this.buildTemplate(jobDetailsDict[jobId], location);
//    }
//
//
//
//
//
//    this.removeFilter = function (ev) {
//        ev.parentElement.parentElement.parentElement.removeChild(ev.parentElement.parentElement);
//
//        //empty the current html
//        $('#allJobsDetail').html("");
//
//        $(".singleFilter").each(function (index, el) {
//            displayAllJobsByLocation(el.children[0].innerHTML);
//        });
//    };
//}