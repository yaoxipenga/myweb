const API_BASE = 'http://10.17.10.1:5000/api';
let currentPage = 1;
const perPage = 10;
let total = 0;
let currentSearch = '';

const listEl = document.getElementById('movie-list');
const detailEl = document.getElementById('movie-detail');
const backBtn = document.getElementById('back-to-list');
const searchInput = document.getElementById('search-box');
const pageIndicator = document.getElementById('page-indicator');
const pageInput = document.getElementById('page-input');
const jumpBtn = document.getElementById('jump-btn');

function loadMovies(page = 1) {
  const url = `${API_BASE}/movies?page=${page}&per_page=${perPage}&search=${encodeURIComponent(currentSearch)}`;
  fetch(url)
    .then(res => res.json())
    .then(data => {
      total = data.total;
      renderMovies(data.movies);
      updatePagination();
    });
}

function renderMovies(movies) {
  listEl.innerHTML = '';
  detailEl.style.display = 'none';
  movies.forEach(movie => {
    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.textContent = `${movie.title} (${movie.year})`;
    li.addEventListener('click', () => showDetail(movie.title));
    listEl.appendChild(li);
  });
}

function showDetail(title) {
  fetch(`${API_BASE}/movie/${encodeURIComponent(title)}`)
    .then(res => res.json())
    .then(data => {
      listEl.innerHTML = '';
      detailEl.style.display = 'block';
      document.getElementById('detail-title').textContent = data.title;
      document.getElementById('detail-director').textContent = data.director;
      document.getElementById('detail-rating').textContent = data.rating;
      document.getElementById('detail-description').textContent = data.description;
    });
}

function updatePagination() {
  pageIndicator.textContent = `第 ${currentPage} 页 / 共 ${Math.ceil(total / perPage)} 页`;
  pageInput.value = currentPage;
}

document.getElementById('prev-page').addEventListener('click', () => {
  if (currentPage > 1) {
    currentPage--;
    loadMovies(currentPage);
  }
});

document.getElementById('next-page').addEventListener('click', () => {
  if (currentPage < Math.ceil(total / perPage)) {
    currentPage++;
    loadMovies(currentPage);
  }
});

document.getElementById('first-page').addEventListener('click', () => {
  currentPage = 1;
  loadMovies(currentPage);
});

document.getElementById('last-page').addEventListener('click', () => {
  currentPage = Math.ceil(total / perPage);
  loadMovies(currentPage);
});

backBtn.addEventListener('click', () => {
  detailEl.style.display = 'none';
  loadMovies(currentPage);
});

searchInput.addEventListener('input', () => {
  currentSearch = searchInput.value.trim();
  currentPage = 1;
  loadMovies(currentPage);
});

jumpBtn.addEventListener('click', () => {
  const targetPage = parseInt(pageInput.value);
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= Math.ceil(total / perPage)) {
    currentPage = targetPage;
    loadMovies(currentPage);
  } else {
    alert('请输入有效的页码');
  }
});

loadMovies();
