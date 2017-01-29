document.addEventListener("DOMContentLoaded", function(event) { 
(function() {
  var animating = false;

  function animatecard(ev) {
    if (animating === false) {
      var t = ev.target;
      if (t.className === 'but-nope') {
        t.parentNode.classList.add('nope');
        animating = true;
        fireCustomEvent('nopecard',
          {
            origin: t,
            container: t.parentNode,
            card: t.parentNode.querySelector('.card')
          }
        );
      }
      if (t.className === 'but-yay') {
        t.parentNode.classList.add('yes');
        animating = true;
        fireCustomEvent('yepcard',
          {
            origin: t,
            container: t.parentNode,
            card: t.parentNode.querySelector('.card')
          }
        );
      }
      if (t.classList.contains('current')) {
        fireCustomEvent('cardchosen',
          {
            container: getContainer(t),
            card: t
          }
        );
      }
    }
  }

  function fireCustomEvent(name, payload) {
    var newevent = new CustomEvent(name, {
      detail: payload
    });
    document.body.dispatchEvent(newevent);
  }

  function getContainer(elm) {
    var origin = elm.parentNode;
    if (!origin.classList.contains('cardcontainer')){
      origin = origin.parentNode;
    }
    return origin;
  }

  function animationdone(ev) {
    animating = false;
    var origin = getContainer(ev.target);
    if (ev.animationName === 'yay') {
      origin.classList.remove('yes');
    }
    if (ev.animationName === 'nope') {
      origin.classList.remove('nope');
    }
    if (origin.classList.contains('list')) {
      if (ev.animationName === 'nope' ||
          ev.animationName === 'yay') {
        origin.querySelector('.current').remove();
        if (!origin.querySelector('.card')) {
          fireCustomEvent('deckempty', {
            origin: origin.querySelector('button'),
            container: origin,
            card: null
          });
        } else {
          origin.querySelector('.card').classList.add('current');
        }
      }
    }
  }
  document.body.addEventListener('animationend', animationdone);
  document.body.addEventListener('webkitAnimationEnd', animationdone);
  document.body.addEventListener('click', animatecard);
  window.addEventListener('DOMContentLoaded', function(){
    document.body.classList.add('tinderesque');
  });
  document.body.addEventListener('nopecard', function(ev) {
      var container = ev.detail.container;
      var label = container.querySelector('.nopes');
      if (label) {
        var nopes = +container.nopes || 0;
        nopes++;
        container.nopes = nopes;
        label.innerHTML = container.nopes;
      }
  });
  document.body.addEventListener('yepcard', function(ev) {
      var container = ev.detail.container;
      var label = container.querySelector('.yays');
      if (label) {
        var yeps = +container.yeps || 0;
        yeps++;
        container.yeps = yeps;
        label.innerHTML = container.yeps;
      }
  });
  document.body.addEventListener('deckempty', function(ev) {
          location.reload();
  });
  function getData(url) {
      var xmlhttp;
      xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function(){
          if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
              JSON.parse(xmlhttp.responseText)["data"].forEach(function(o){
                  cards.add_card(o);
              });
          }
      }
      xmlhttp.open("GET", url, true);
      xmlhttp.send();
  }
  getData("/next_card");
  var cards = {
      started: false,
      add_card: function(data) {
          var container = document.querySelector(".cardlist");
          var li = document.createElement("li");
          li.classList.add("card");
          if (this.started === false) {
              li.classList.add("current");
              this.started = true;
          }
          var img_container = document.createElement("div");
          img_container.classList.add("image_container");
          img_container.style = "background-image: url('" + data["url"] + "')";
          li.appendChild(img_container);
          var content_container = document.createElement("div");
          content_container.classList.add("content_container");
          // Most tedious part is here
          var createDate = document.createElement("span");
          var description = document.createElement("span");
          var dislikes = document.createElement("span");
          var gId = document.createElement("span");
          var likes = document.createElement("span");
          var tags = document.createElement("span");
          var title = document.createElement("span");
          var userName = document.createElement("span");
          createDate.classList.add("c_createDate");
          description.classList.add("c_description");
          dislikes.classList.add("c_dislikes");
          gId.classList.add("c_id");
          likes.classList.add("c_likes");
          tags.classList.add("c_tags");
          title.classList.add("c_title");
          userName.classList.add("c_title");
          createDate.innerText = data["createDate"];
          description.innerText = data["description"];
          dislikes.innerText = data["dislikes"];
          gId.innerText = data["id"];
          likes.innerText = data["likes"];
          data["tags"].forEach(function(tag) {
              var tag_el = document.createElement("span");
              tag_el.innerText = tag;
              tags.appendChild(tag_el);
          });
          title.innerText = data["title"];
          userName.innerText = data["userName"];
          content_container.appendChild(createDate);
          content_container.appendChild(description);
          content_container.appendChild(dislikes);
          content_container.appendChild(gId);
          content_container.appendChild(likes);
          content_container.appendChild(tags);
          content_container.appendChild(title);
          content_container.appendChild(userName);
          // Ends here
          li.appendChild(content_container);
          container.appendChild(li);
          console.log(data);
      }
  };
})();
});
