/* Dore Theme Select & Initializer Script 

Table of Contents

01. Css Loading Util
02. Theme Selector And Initializer
*/

/* 01. Css Loading Util */
function loadStyle(href, callback) {
  for (var i = 0; i < document.styleSheets.length; i++) {
    if (document.styleSheets[i].href == href) {
      return;
    }
  }
  var head = document.getElementsByTagName("head")[0];
  var link = document.createElement("link");
  link.rel = "stylesheet";
  link.type = "text/css";
  link.href = href;
  if (callback) {
    link.onload = function() {
      callback();
    };
  }
  head.appendChild(link);
}
/* 02. Theme Selector And Initializer */
(function($) {
  if ($().dropzone) {
    Dropzone.autoDiscover = false;
  }
  
  var themeColorsDom =
    '<div class="theme-colors"> <div class="p-4"> <p class="text-muted mb-2">Light Theme</p> <div class="d-flex flex-row justify-content-between mb-4"> <a href="#" data-theme="dore.light.blue.min.css" class="theme-color theme-color-blue"></a> <a href="#" data-theme="dore.light.purple.min.css" class="theme-color theme-color-purple"></a> <a href="#" data-theme="dore.light.green.min.css" class="theme-color theme-color-green"></a> <a href="#" data-theme="dore.light.orange.min.css" class="theme-color theme-color-orange"></a> <a href="#" data-theme="dore.light.red.min.css" class="theme-color theme-color-red"></a> </div> <p class="text-muted mb-2">Dark Theme</p> <div class="d-flex flex-row justify-content-between"> <a href="#" data-theme="dore.dark.blue.min.css" class="theme-color theme-color-blue"></a> <a href="#" data-theme="dore.dark.purple.min.css" class="theme-color theme-color-purple"></a> <a href="#" data-theme="dore.dark.green.min.css" class="theme-color theme-color-green"></a> <a href="#" data-theme="dore.dark.orange.min.css" class="theme-color theme-color-orange"></a> <a href="#" data-theme="dore.dark.red.min.css" class="theme-color theme-color-red"></a> </div> </div> <a href="#" class="theme-button"> <i class="simple-icon-magic-wand"></i> </a> </div>';
  $("body").append(themeColorsDom);
  var theme = "dore.light.blue.min.css";

  if (typeof Storage !== "undefined") {
    if (localStorage.getItem("theme")) {
      theme = localStorage.getItem("theme");
    }
  }

  $(".theme-color[data-theme='" + theme + "']").addClass("active");

  console.log(window.location.pathname)
  loadStyle("../static/css/" + theme, onStyleComplete);
  function onStyleComplete() {
    setTimeout(onStyleCompleteDelayed, 300);
  }

  function onStyleCompleteDelayed() {
    var $dore = $("body").dore();
  }

  $("body").on("click", ".theme-color", function(event) {
    event.preventDefault();
    var dataTheme = $(this).data("theme");
    if (typeof Storage !== "undefined") {
      localStorage.setItem("theme", dataTheme);
      window.location.reload();
    }
  });


  $(".theme-button").on("click", function(event) {
    event.preventDefault();
    $(this)
      .parents(".theme-colors")
      .toggleClass("shown");
  });
  $(document).on("click", function(event) {
    if (
      !(
        $(event.target)
          .parents()
          .hasClass("theme-colors") ||
        $(event.target)
          .parents()
          .hasClass("theme-button") ||
        $(event.target).hasClass("theme-button") ||
        $(event.target).hasClass("theme-colors")
      )
    ) {
      if ($(".theme-colors").hasClass("shown")) {
        $(".theme-colors").removeClass("shown");
      }
    }
  });
})(jQuery);
