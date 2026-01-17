let tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

const setsGrid = document.getElementById("sets-grid");
const productsGrid = document.getElementById("products-grid");

// Примеры данных (для курсовой достаточно демо).
// Если хотите — можно генерировать data.json скриптом save_as_static.py и подгружать по fetch().
const SETS = [
  { id: 1, name: "Набор начинающего гитариста", description: "Гитара + тюнер + кабель", duration: "Старт", places_count: 3 },
  { id: 2, name: "Домашняя мини-студия", description: "Запись дома: микрофон + интерфейс", duration: "Запись", places_count: 3 },
  { id: 3, name: "Пианино для занятий", description: "Выбор для обучения дома", duration: "Учёба", places_count: 3 },
];

const PRODUCTS = [
  { id: 1, name: "Yamaha F310", description: "Акустическая гитара для обучения", address: "Yamaha • акустическая", price: "79 900 ₸" },
  { id: 6, name: "Yamaha P-45", description: "Цифровое пианино 88 клавиш", address: "Yamaha • пианино", price: "279 000 ₸" },
  { id: 9, name: "Alesis Nitro Mesh Kit", description: "Электронные барабаны (mesh)", address: "Alesis • барабаны", price: "259 000 ₸" },
  { id: 18, name: "Shure SM58", description: "Вокальный микрофон", address: "Shure • микрофон", price: "79 000 ₸" },
];

function generatePlaceholder(id, type) {
  const color = type === "set" ? "#8B5CF6" : "#3B82F6";
  const title = type === "set" ? "Набор" : "Товар";
  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" class="card-svg">
      <rect width="800" height="600" fill="${color}"/>
      <text x="400" y="300" font-size="72" fill="white" text-anchor="middle" font-family="sans-serif">${title}</text>
      <text x="400" y="380" font-size="56" fill="#ddd" text-anchor="middle" font-family="sans-serif">#${id}</text>
    </svg>
  `;
}

function renderSets() {
  setsGrid.innerHTML = SETS.map(s => `
    <div class="card" onclick="selectSet(${s.id}, this)">
      <div class="card-image">${generatePlaceholder(s.id, "set")}</div>
      <div class="card-content">
        <div class="card-title">${s.name}</div>
        <div class="card-desc">${s.description}</div>
        <div class="card-meta">
          <span>${s.duration}</span>
          <span class="badge">${s.places_count} поз.</span>
        </div>
      </div>
    </div>
  `).join("");
  productsGrid.innerHTML = "";
  tg.MainButton.hide();
}

function renderProducts() {
  productsGrid.innerHTML = PRODUCTS.map(p => `
    <div class="card" onclick="selectProduct(${p.id}, this)">
      <div class="card-image">${generatePlaceholder(p.id, "product")}</div>
      <div class="card-content">
        <div class="card-title">${p.name}</div>
        <div class="card-desc">${p.description}</div>
        <div class="card-meta">
          <span>${p.address}</span>
          <span class="badge">${p.price}</span>
        </div>
      </div>
    </div>
  `).join("");
  setsGrid.innerHTML = "";
  tg.MainButton.hide();
}

window.selectSet = function (id, el) {
  const name = el.querySelector(".card-title").textContent;
  tg.MainButton.setText(`Открыть набор: ${name}`).show();
  tg.MainButton.offClick();
  tg.MainButton.onClick(() => {
    tg.sendData(JSON.stringify({ action: "open_route", route_id: id }));
    tg.close();
  });
};

window.selectProduct = function (id, el) {
  const name = el.querySelector(".card-title").textContent;
  tg.MainButton.setText(`Открыть товар: ${name}`).show();
  tg.MainButton.offClick();
  tg.MainButton.onClick(() => {
    tg.sendData(JSON.stringify({ action: "open_attraction", attraction_id: id }));
    tg.close();
  });
};

// Табы
document.querySelectorAll(".tab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");

    if (tab.dataset.tab === "sets") renderSets();
    else renderProducts();
  };
});

renderSets();
