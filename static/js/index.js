let bookContainer = document.querySelector(".search");
let searchBooks = document.getElementById("search-box");
let searchBooksByTitle = document.getElementById("search-by-title");
let searchBooksByAuthors = document.getElementById("search-by-authors");
let searchBooksByPublisher = document.getElementById("search-by-publisher");
let searchBooksByCategories = document.getElementById("search-by-categories");

const pathname = window.location.pathname;
const pageName = pathname.substring(1, pathname.length - 1);
console.log("pageName", pageName);
const url = "http://127.0.0.1:8000";

const getBooks = async () => {
  const response = await fetch(
    `${url}/search_book/?q=${searchBooks.value}&title=${searchBooksByTitle.value}&authors=${
      searchBooksByAuthors.value}&categories=${searchBooksByCategories.value}&publisher=${searchBooksByPublisher.value}`
  );
  const data = await response.json();
  console.log("daaattaa", data);
  return data;
};

const extractThumbnail = ({ imageLinks }) => {
  const DEFAULT_THUMBNAIL = "icons/logo.svg";
  if (!imageLinks || !imageLinks.thumbnail) {
    return DEFAULT_THUMBNAIL;
  }
  return imageLinks.thumbnail.replace("http://", "https://");
};
const verifyValue = (value)=>{
  return value && typeof value !== 'undefined' && value !== null
    ? (typeof value === 'string'
      ? `'${value.replace(/['"‘’“”]/g, ' ')}'`
      : `'${value}'`)
    : null;
}
const drawListBook = async () => {
  console.log("drawListBook");
  if (searchBooks.value != "" || searchBooksByAuthors.value != "" || searchBooksByCategories.value != "" || searchBooksByPublisher.value != "" || searchBooksByTitle.value != "") {
    bookContainer.style.display = "flex";
    bookContainer.innerHTML = `<div class='prompt'><div class="loader"></div></div>`;
    const data = await getBooks();
    console.log("datatttat",data);
    if (data.error) {
      bookContainer.innerHTML = `<div class='prompt'>ツ Limit exceeded! Try after some time</div>`;
    } else if (data.totalItems == 0) {
      bookContainer.innerHTML = `<div class='prompt'>ツ No results, try a different term!</div>`;
    } else if (data.totalItems == undefined) {
      bookContainer.innerHTML = `<div class='prompt'>ツ Network problem!</div>`;
    } else {
      bookContainer.innerHTML = data.items
        .map(
          (bookData) => {
            const volumeInfo = bookData.volumeInfo;
            const publisherContent = volumeInfo.publisher && volumeInfo.publisher !== 'undefined' ? `<div class='book-publisher' onclick='updateFilter(this,"publisher");'>${volumeInfo.publisher}</div>` : '';
            const totalLikes = bookData.total_likes || 0;
            const totalComments = bookData.total_comments || 0;
            const totalRecommendations = bookData.total_recommendations || 0;
            console.log("checkkkk", totalLikes, totalComments, totalRecommendations);
            const title = verifyValue(volumeInfo.title);
            // const previewLink = verifyValue(volumeInfo.previewLink);
            const authors = verifyValue(volumeInfo.authors);
            const categories = verifyValue(volumeInfo.categories);
            const publisher = verifyValue(volumeInfo.publisher);
            const publishedDate = verifyValue(volumeInfo.publishedDate);
            const description = verifyValue(volumeInfo.description);
            const googleBookId = verifyValue(bookData.id);
            const ratingsCount = verifyValue(volumeInfo.ratingsCount);
            const thumbnail = verifyValue(extractThumbnail(volumeInfo));

            console.log("publishedDate", publishedDate);
            const likeFunction = `onclick="likeBook(${title}, ${authors}, ${categories}, ${publisher}, ${publishedDate}, ${googleBookId}, ${ratingsCount}, ${description}, ${thumbnail});"`
            const recommedFunction = `onclick="recommendBook(${title}, ${authors}, ${categories}, ${publisher}, ${publishedDate}, ${googleBookId}, ${ratingsCount}, ${description}, ${thumbnail});"`

            return `<div class='book-wo-flex' style='background: linear-gradient(` +
            getRandomColor() +
            `, rgba(0, 0, 0, 0));'><div style="width: 100%; display: flex; justify-content: end">
            <button ${recommedFunction} class="like-or-comment">${totalRecommendations} 💡</button></div><div class="flex">`+
              `<a href='${volumeInfo.previewLink}' target='_blank'><img class='thumbnail' src='` +
              extractThumbnail(volumeInfo) +
            `' alt='cover'></a><div class='book-info'><h3 class='book-title'>
            <div class='title' onclick='updateFilter(this,"title");'>` +
              `${volumeInfo.title}</div>
              </h3><div class='book-authors' onclick='updateFilter(this,"author");'>`+
              `${volumeInfo.authors}</div>`+
              publisherContent +
            `<div class='info' onclick='updateFilter(this,"subject");' style='background-color: ` +
            getRandomColor() +
            `;'>` +
              (!volumeInfo.categories || volumeInfo.categories === undefined
              ? "Others"
              : volumeInfo.categories) +
            `</div>
            <div class="like-or-comment-container d-flex-sb">
              <button class="like-or-comment" ${likeFunction}>
                  ${totalLikes} 👍
              </button>
              <button class="like-or-comment" onclick="openCommentSection('${bookData.id}')">
                  <p class="comment">${totalComments}</p> 💬
              </button>
          </div>
            <div method="post" id="comment-${bookData.id}" style="display: none; width: 100%;">
              <input id="comment-input-${bookData.id}" style="
                width: 100%;
                border-radius: 25px;
                padding: 10px 20px;
                margin-bottom: 8px;
    border: 1px solid;
                " type="text"/>
              <button onclick="commentBook('${bookData.id}')" class='info' style="background-color: #25cc8c40;">Send</button>
          </div>
            </div></div>
            </div>`}
        )
        .join("");
    }
  } else {
    bookContainer.style.display = "none";
  }
};

const updateFilter = ({ innerHTML }, f) => {
  document.getElementById("main").scrollIntoView({
    behavior: "smooth",
  });

  console.log("innerHTML", innerHTML)
  switch (f) {
    case "author":
      searchBooksByAuthors.value = innerHTML;
      break;
    case "subject":
      searchBooksByCategories.value = innerHTML;
      break;
    case "publisher":
      searchBooksByPublisher.value = innerHTML;
      break;
    case "title":
      searchBooksByTitle.value = innerHTML;
      break;
  }
  console.log('calling drawListBook');
  debounce(drawListBook, 1000);
  showFilters({  target: {checked: true} });
};
const debounce = (fn, time, to = 0) => {
  to ? clearTimeout(to) : (to = setTimeout(drawListBook, time));
};

if (searchBooks){
  searchBooks.addEventListener("input", () => debounce(drawListBook, 1000));
  searchBooksByAuthors.addEventListener("input", () => debounce(drawListBook, 1000));
  searchBooksByCategories.addEventListener("input", () => debounce(drawListBook, 1000));
  searchBooksByPublisher.addEventListener("input", () => debounce(drawListBook, 1000));
  searchBooksByTitle.addEventListener("input", () => debounce(drawListBook, 1000));
}

const getRandomColor = () =>
  `#${Math.floor(Math.random() * 16777215).toString(16)}40`;


const toggleSwitch = document.querySelector(
  '.theme-switch input[type="checkbox"]'
);
if (localStorage.getItem("marcdownTheme") == "dark") {
  document.documentElement.setAttribute("data-theme", "dark");
  document
    .querySelector("meta[name=theme-color]")
    .setAttribute("content", "#090b28");
  toggleSwitch.checked = true;
  localStorage.setItem("marcdownTheme", "dark");
} else {
  document.documentElement.setAttribute("data-theme", "light");
  document
    .querySelector("meta[name=theme-color]")
    .setAttribute("content", "#ffffff");
  toggleSwitch.checked = false;
  localStorage.setItem("marcdownTheme", "light");
}
const switchTheme = ({ target }) => {
  if (target.checked) {
    document.documentElement.setAttribute("data-theme", "dark");
    document
      .querySelector("meta[name=theme-color]")
      .setAttribute("content", "#090b28");
    localStorage.setItem("marcdownTheme", "dark");
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    document
      .querySelector("meta[name=theme-color]")
      .setAttribute("content", "#ffffff");
    localStorage.setItem("marcdownTheme", "light");
  }
};
toggleSwitch.addEventListener("change", switchTheme, false);


const filterSwitch = document.querySelector('.filter-switch input[id="checkbox"]');
const showFilters = ({ target }) => {
  console.log("showFilterssss", target.checked);
  if (target.checked) {
    document.getElementById('use-filters').style.display = 'block';
    document.getElementById('search-box').style.display = 'none';
    document.getElementById('use-filter-text').style.display = 'none';
    document.getElementById('input-container').style.alignItems = 'start';
  } else {
    document.getElementById('use-filters').style.display = 'none';
    document.getElementById('search-box').style.display = 'block';
    document.getElementById('use-filter-text').style.display = 'block';
    document.getElementById('input-container').style.alignItems = 'center';
  }
};

if(filterSwitch){
  filterSwitch.addEventListener("change", showFilters, false);
}

const likeBook = async (title, authors, categories, publisher, publishedDate, googleBookId, ratingsCount, description, thumbnail) => {
  const book = {
    title: title,
    authors: authors,
    genre: categories, 
    publisher: publisher,
    publishedDate: publishedDate,
    description: description,
    googleBookId: googleBookId,
    ratingsCount: ratingsCount,
    thumbnail: thumbnail,
  }
  const response = await fetch(
    `${url}/like_book/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(book)
  }
  );
  const responseData = await response.json();
  console.log("responseData: ", responseData);
  window.location.href = "/likes/";
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// liked by user

document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav.scrolltoview");

  navLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("current");
    }
  });
});

const openCommentSection = (id) => {
  console.log("openCommentSection", id)
  if (document.getElementById(`comment-${id}`).style.display === "block") {
    document.getElementById(`comment-${id}`).style.display = "none";
  }
  else {
    document.getElementById(`comment-${id}`).style.display = "block";
  }
};


const commentBook = async (id) => {
  try {
    const comment = document.getElementById(`comment-input-${id}`).value;
    await fetch(
      `${url}/comment/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCookie('csrftoken'),
      },
        body: JSON.stringify({ google_book_id: id, comment: comment }),
    });
    window.location.href = "/likes/";
  } catch (error) {
    console.error('Error:', error);
  }
}

const recommendBook = async (title, authors, categories, publisher, publishedDate, googleBookId, ratingsCount, description, thumbnail) => {
  try {
    const book = {
      title: title,
      authors: authors,
      genre: categories,
      publisher: publisher,
      publishedDate: publishedDate,
      description: description,
      googleBookId: googleBookId,
      ratingsCount: ratingsCount,
      thumbnail: thumbnail,
    }
    await fetch(
      `${url}/recommendations/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(book),
    });
    window.location.href = "/recommendations/";
  } catch (error) {
    console.error('Error:', error);
  }
}
