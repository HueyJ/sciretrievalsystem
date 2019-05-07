String.prototype.replaceAllWithStrong = function(search) {
    var target = this;
	var replacement = "<strong>$1</strong>"
    return target.replace(new RegExp("(" + search + ")", 'gi'), replacement);
};

$(document).ready(function() {

	var currPage = 0;
	var scrolled = false;
	var scroll = true;
    var facetLoaded = false;
    // var paginized = false;

    $(window).resize(function() {
        $("#navbar").attr("style", "height=100%");
        replacePageNav();
    });

	if (!$("#result").html() && $("#result-list").html()) {
		getCurrResults(300, -1);
	}

	$(window).scroll(function() {
		// location of top
		var scrollTop = $(window).scrollTop();
		// height of window
		var windowHeight = $(window).height();
		// height of document
		var documentHeight = $(document).height();
		// 100 before touch the bottom
		var loadHeight = scrollTop + windowHeight + 100;
		toggleElement(".go-top", scrollTop, loadHeight, documentHeight);
		// toggleElement("#page-nav", scrollTop, loadHeight, documentHeight);
        if (loadHeight >= documentHeight && currPage < $("#page").text()) {
            if (scroll) {
                if (!scrolled) {
                    scrolled = true;
                }
                getCurrResults(1200, loadHeight - 500);
            }
        }
        if (loadHeight >= documentHeight && currPage == $('#page').text()
        && scroll) {
            $("#result-list").append(
                "<div " +
                "class='alert alert-warning alert-dismissible fade in' " +
                "role='alert'>" +
                "<button " +
                "type='button'" +
                "class='close'" +
                "data-dismiss='alert'" +
                "aria-label='Close'>" +
                "<span aria-hidden='true'>×</span>" +
                "</button>" +
                "It is the end!" +
                "</div>"
            );
            // end of all the results, never scroll down again.
            if (scroll) {
                scroll = false;
            }
        }
	});

	// display or hide elements
	function toggleElement(element, scrollTop, loadHeight, documentHeight) {
        if (scrollTop > 200) {
			$(element).fadeIn(300);
		} else if (loadHeight >= documentHeight || scrollTop <= 200) {
			$(element).fadeOut(300);
		}
        // replacePageNav();
	}

    // load the search results of current page
	function getCurrResults(renderSpeed, loadHeight) {
		// lock scroll
		if (scroll) {
			scroll = false;
		}
		$.get(
			"/aquery/" + $("title").html() + "/" + nextPage(),
			function(response) {
				var resp = JSON.parse(response)
				var results = JSON.parse(resp["results"]);
                var facet = JSON.parse(resp["facet"]);
                var pageNum = resp["pageNum"];
				var rendering = "";

				$("#page").html(pageNum);
                // if (!paginized) {
                //     paginize(pageNum);
                // }
                if (!facetLoaded) {
                    var numberOfLabel = 3;
                    for (var items in facet) {
                        if (facet.hasOwnProperty(items)) {
                            navPills = "" +
                            "<ul class='nav nav-pills nav-stacked'>" +
                                "<h5>" + items + ": </h5>";
                            var counter = 0;
                            if (items == "Year") {
                                var item = Object.keys(facet[items]).sort().reverse();
                                for (var i = 0; i < item.length; i++) {
                                    if (i < numberOfLabel) {
                                        navPills += "" +
                                        "<li><a href='#'>" + item[i] + "(" + facet[items][item[i]] + ")</a></li>";
                                    }
                                }
                                counter = item.length;
                            } else if (items == "Openaccess") {
                                for (var item in facet[items]) {
                                    if (counter < numberOfLabel) {
                                        if (item == 1) {
                                            label = "Full Article";
                                        } else {
                                            label = "Abstract Only";
                                        }
                                        navPills +=
                                        "<li><a href='#'>" + label + "(" + facet[items][item] + ")</a></li>";
                                    }
                                    counter++;
                                }
                            } else {
                                for (var item in facet[items]) {
                                    if (counter < numberOfLabel) {
                                        navPills +=
                                        "<li><a href='#'>" + item + "(" + facet[items][item] + ")</a></li>";
                                    }
                                    counter++;
                                }
                            }
                            if (counter > numberOfLabel) {
                                navPills += "<li><a href='#'>...</a></li>";
                            }
                            navPills += "</ul>";
                            $("#navbar").append(navPills);
                        }
                    }
                    facetLoaded = true;
                }

				for (var i = 0; i < results.length; i++) {
					rendering += renderResult(results[i]._source);
				}
                $("#result-list").append(
                    "<hr id='page-anchor" + currPage +
                    "' class='page-placeholder'>"
				);
                $("#result-list").append(
					"<div id='page" + currPage + "' hidden>" +
						rendering +
					"</div>"
				);
				$("#page" + currPage).fadeIn(renderSpeed);
                if (loadHeight !== -1) {
                    $('html, body').animate({scrollTop: loadHeight+200}, 300);
                }
				// release lock
				if (!scroll) {
					scroll = true;
				}
			}
		);

	}

	function nextPage() {
		return ++currPage;
	}

    // function paginize(pageNum) {
        // for (var i = 1; i <= pageNum; i++) {
        //     page = "<li";
        //     if (i == currPage) {
        //         page += " class='active'";
        //     }
        //     page += ">";
        //     page += "<a href='#page-anchor" + i + "'>";
        //     page += i
        //     if (i == currPage) {
        //         page += " <span class='sr-only'>(current)</span>";
        //     }
        //     page += "</a></li>";
        //     $("#page-placeholder").before(page);
        // }
        // paginized = true;
    // }

	function renderResult(result) {
		if (parseInt(result.openaccess)) {
			theme = "-success";
			openaccess = "Open access"
		} else {
			theme = "-default";
			openaccess = "Abstract only"
		}

		id = result.id;
		href = result.href;
		title = result.title;
		author = result.author;
		abstract = result.abstract;
		subject = result.subject;

		searchTerms = $("#search").val();

		// shade search terms
		subject = shade(subject, searchTerms);
		author = shade(author, searchTerms);
		abstract = shade(abstract, searchTerms);
		if (result.id == searchTerms
			|| result.pii == searchTerms
			|| result.doi == searchTerms
			|| result.eid == searchTerms) {
				title = shade(title, title);
		} else {
			title = shade(title, searchTerms);
		}

		r = "";
		r += "<div id='result' class='panel panel" + theme + "'>";
		// Default panel content;
		r += "<div class='panel-heading'>";
		r += "<h3 class='panel-title'>";
		r += "<a href='" + href + "'>";
		r += 				title;
		r += 			"</a>";
		r += 		"</h3>";
		r += 	"</div>";
		// List group
		r += 	"<ul class='list-group'>";
		r += 		"<li class='list-group-item'>" + author + "</li>";
		r += 	"</ul>";
		r += 	"<div class='panel-body'>";
		r += 		"<a ";
		r += 			"data-toggle='collapse'";
		if (abstract) r += "href='#" + id + "-abstract'";
		r += 		">";
		r += 			"Abstract";
		r += 		"</a>";
		r += 		"<br>";
		r += 		"<div id='" + id + "-abstract' class='collapse'>";
		r += 			abstract;
		r += 		"</div>";
		r += 	"</div>";
		r += 	"<div class='panel-footer'>" + subject + "</div>";
		r += "</div>";
		return r;
	}

	function shade(text, terms) {
		if (!text) {
			return "";
		}
		text = text.trim();
		text = text.replaceAllWithStrong(terms);
		if (!terms.split(" ") == terms) {
			terms = terms.split(" ");
			for (var i = 0; i < terms.length; i++) {
				term = terms[i];
				if (term) {
					text = text.replaceAllWithStrong(term);
				}
			}
		}
		return text;
	}

    // To keep the #page-nav always in the middle of #result-list
    // function replacePageNav() {
    //     $("#page-nav").css(
    //         "left",
    //         $(window).width() / 2 - $("#page-nav").width() / 2
    //     );
    // }

    // Animate the scroll to top
    $(".go-top").click(function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, 300);
    });

	$("#search").on('input propertychange', function(event){
		query_expression = "/" + encodeURIComponent($("#search").val());
		query_expression = query_expression.replace(".", "&#46");
		$("form").attr("action", "/query" + query_expression);
	});

});
