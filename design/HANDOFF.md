# Handoff: IFFECTA Landing — розовая пенка IFF-01

## Overview
Одностраничный лендинг пенки для умывания IFFECTA (розовая, IFF-01) + 4 технические страницы (Политика конфиденциальности, Пользовательское соглашение, Согласие на обработку ПД, Оферта). Задача лендинга — эмоционально представить продукт, показать состав и применение, познакомить с линейкой (3 цвета) и увести на покупку в Wildberries. Адаптив desktop → mobile.

Роуты: `/` лендинг, `/privacy`, `/terms`, `/consent`, `/offer` (имена на усмотрение разработчика).

## About the Design Files
Файлы в этом пакете — **дизайн-референсы, собранные в HTML** (`IFFECTA Landing.dc.html` + `IFFECTA Landing Mobile.dc.html`). Это прототип, показывающий внешний вид и поведение, а не продакшн-код для копирования. Задача — **воссоздать дизайн в стеке целевого проекта** (Next.js/React, Astro, Tilda-кастом, чистый HTML+CSS — что принято в кодовой базе). Если стека ещё нет — подойдёт статический Next.js/Astro с одним роутом; зависимостей, кроме шрифта, у дизайна нет.

`IFFECTA Landing Mobile.dc.html` — лишь обёртка-телефон с `<iframe>` на основной файл для превью; в реализации не нужна.

Внутренности `.dc.html`: разметка лежит внутри `<x-dc>…</x-dc>`, стили инлайновые, `style-hover="…"` — это hover-состояние элемента (перенести в `:hover`). Атрибуты `data-m-*` помечают элементы, к которым применяются мобильные правила из `@media (max-width:640px)` в `<style>` вверху файла. Скрипт `support.js` / `image-slot.js` — рантайм прототипа, не переносить.

## Fidelity
**High-fidelity.** Цвета, типографика, отступы, радиусы, состояния — финальные. Воспроизводить точно, используя значения ниже. Тексты — финальные, не переписывать.

## Page structure (сверху вниз)

Весь контент — внутри страницы с фоном `#F7C7DD` и внешним паддингом `clamp(12px,3vw,40px)`. Основной контент — белая карточка `max-width:1280px`, `border-radius:20px`, `overflow:hidden`, по центру. Футер — отдельная белая карточка под ней (`margin-top:16px`, radius 16px).

### 1. Header (вне белой карточки)
- flex, space-between, `padding: 6px 4px 22px`, `max-width:1280px`, по центру, `flex-wrap`.
- Слева: логотип `logo-oneline-black.png`, высота 22px.
- Центр: nav, 4 якорные ссылки 14px/500: «О пенке» `#about`, «Состав» `#actives`, «Применение» `#how`, «Линейка» `#lineup`. Gap `clamp(14px,2.5vw,32px)`.
- Справа: кнопка «Купить» → `#buy`. Чёрная пилюля `#151515`, текст `#fff`, `padding:10px 18px`, radius 999, 14px/500. Hover: фон `#F52A82`.
- **Mobile (≤640):** nav скрыт, паддинг `4px 2px 14px`; остаются логотип и кнопка.

### 2. Hero (`data-screen-label="Hero"`)
- Блок `position:relative`, высота `clamp(520px,78vh,800px)`. **Mobile:** высота auto, `aspect-ratio:3/4`.
- Подложка: фото `photos/web/1028.jpg`, `object-fit:cover`, `object-position:50% 0%` (важно — лицо вверху кадра).
- Поверх фото — `<video muted loop playsinline preload="auto">`, `object-fit:cover`, `opacity:0`, `transition:opacity .6s`. Источник выбирается по `matchMedia('(max-width:640px)')`: `hero-mobile.mp4` (1080×1920) или `hero-desktop.mp4`. См. «Interactions».
- Оверлей `position:absolute; inset:0; padding:clamp(16px,3vw,36px)`, flex column, `justify-content:space-between`, `pointer-events:none` (интерактивные дети — `pointer-events:auto`).
  - **Верх, слева — стеклянная карточка** (desktop only, на mobile скрыта): `width:min(300px,100%)`, `background:rgba(255,255,255,.55)`, `backdrop-filter:blur(14px)`, `border:1px solid rgba(255,255,255,.7)`, radius 14, `padding:18px 18px 20px`, `box-shadow:0 10px 40px rgba(21,21,21,.08)`. Внутри: розовый кружок 28px `#F52A82` в правом верхнем углу (top/right 14px); лейбл «Эмоции first!» 11px/700, `letter-spacing:.12em`, uppercase, `#F52A82`, `margin-bottom:8px`; абзац 13px/1.45, `max-width:230px`: «Цветная пена превращает обычное умывание в момент, который хочется попробовать, рассмотреть и снять.»
  - **Низ** — flex row, `align-items:flex-end`, space-between, gap 16, wrap. Слева H1 «Умывайся<br>в цвете.»: `clamp(44px,8.5vw,120px)`, weight 800, `line-height:.92`, `letter-spacing:-.04em`, цвет `#F52A82`. Справа кнопка «Купить» → `#buy`: фон `#F52A82`, белый текст, `padding:16px 28px`, radius 999, 15px/700, `letter-spacing:-.01em`, `box-shadow:0 10px 30px rgba(245,42,130,.3)`. Hover: фон `#151515`.
  - **Mobile:** нижний блок становится column, прижат к низу (`margin-top:auto`), кнопка на всю ширину, текст по центру.

### 3. About (`#about`, «Манифест»)
- Grid `repeat(auto-fit, minmax(min(100%,300px),1fr))`, gap `clamp(24px,4vw,56px)`, `align-items:end`, padding `clamp(40px,6vw,88px) clamp(16px,4vw,56px)`.
- Колонка 1: фото `photos/web/0835.jpg`, `aspect-ratio:4/5`, radius 16, `object-fit:cover`, `object-position:50% 0%`.
- Колонка 2 (flex column, gap 20, `padding-bottom:8px`):
  - Абзац 1 (`clamp(15px,1.3vw,18px)`/1.5, `max-width:460px`): «**IFFECTA** — это уход, который начинается с эмоции. Мы сделали пенку, с которой хочется умываться.» Слово IFFECTA — `#F52A82`, 700.
  - Абзац 2: «Мы превращаем простое действие в удовольствие: цветная пена, живая реакция, настроение на весь день.»
  - Лейбл «Розовая пенка» (11px/700/.12em/uppercase/`#F52A82`, `margin-bottom:6px`), H2 «Да, пена розовая.<br>Нет, это не фильтр.» — `clamp(40px,6.5vw,96px)`, 800, `line-height:.95`, `letter-spacing:-.04em`, `#F52A82`.
- **Mobile:** оба абзаца выводятся **перед фото**, затем фото, затем лейбл + H2. (В прототипе — дублированный блок с переключением display; в реализации сделать через `order` или условный рендер.)

### 4. Benefits («Яркое очищение»)
- Тот же grid, padding `0 clamp(16px,4vw,56px) clamp(40px,6vw,88px)`, `align-items:start`.
- Колонка 1 (flex column, gap 28, `padding-top:12px`): лейбл «Яркое очищение»; список из 4 пунктов (`clamp(17px,1.6vw,22px)`/1.35/500, gap 14), маркер — кружок 12px `#F52A82` с `margin-top:9px`:
  1. очищает от излишков себума и загрязнений
  2. поддерживает защитный барьер кожи
  3. деликатно отшелушивает и освежает цвет лица
  4. сохраняет кожу нежной и мягкой
  
  Кнопка-outline «Хочу попробовать» → `#buy`: `border:1.5px solid #F52A82`, текст `#F52A82`, `padding:12px 22px`, radius 999, 14px/500. Hover: фон `#F52A82`, текст белый.
- Колонка 2: фото `photos/web/1084.jpg`, `aspect-ratio:1/1` (**mobile: 3/4**), radius 16, `object-fit:cover`, `object-position:50% 20%`. В **правом нижнем** углу (offset `clamp(12px,2vw,24px)`) — стеклянная карточка как в hero, `width:min(260px,70%)`: лейбл «Вкусный аромат», текст «Ощущение комфорта после умывания. Для ежедневного ухода.» (13px/1.45).

### 5. Actives (`#actives`, «Что внутри»)
- Grid с gap `clamp(24px,3vw,40px)`, padding как у Benefits.
- H2 «Что внутри» — `clamp(34px,4.5vw,64px)`, 800, lh 1, ls -.03em, `#151515`.
- **Карточка лотоса:** фон `#F7C7DD`, radius 16, grid 2 колонки (`minmax(min(100%,300px),1fr)`). Слева — `<video autoplay muted loop playsinline>` `uploads/generated_video.mp4`, `min-height:clamp(320px,45vw,520px)`, cover. Справа — padding `clamp(24px,4vw,48px)`, flex column центр, gap 18: лейбл «Главный ингредиент», H3 «Экстракт розового лотоса» (`clamp(32px,4vw,56px)`, 800, lh .98, ls -.03em, `#F52A82`), абзац `clamp(16px,1.4vw,19px)`/1.45, `max-width:420px`: «Богат антиоксидантами, успокаивает и защищает кожу.»
- Лейбл «Также в составе» (11px/700/.12em/uppercase, `#151515`, `margin-top:8px`).
- **3 карточки** grid `minmax(min(100%,240px),1fr)`, gap 12. Каждая: фон `#F7C7DD`, radius 16, padding 22, flex column gap 14, `min-height:260px`. Сверху картинка высотой 120px, radius 12, белый фон под ней. Заголовок 12px/700/.1em/uppercase/`#F52A82`; текст 14px/1.45.
  1. `uploads/pasted-1792620365162-0.jpg` — «Экзосомы центеллы азиатской» — «сохраняет кожу увлажнённой, уменьшает видимость пор»
  2. `uploads/image (1).jpg` — «Ниацинамид» — «поддерживает защитный барьер кожи, устраняет чувство стянутости»
  3. `uploads/image (2).jpg` — «Фруктовые энзимы» — «бережно отшелушивают ороговевшие клетки эпидермиса»
- **Аккордеон** `<details>`: фон `#F7C7DD`, radius 16, padding `18px 22px`. Summary: «Полный состав» (14px/700/.06em/uppercase) слева, «+» `#F52A82` справа, без дефолтного маркера. Раскрытый текст 13px/1.55, `margin-top:14px`:
  «Aqua, Sodium Cocoyl Glutamate, Disodium Cocoyl Glutamate, Glycerin, Cocamidopropyl Betaine, Annona Cherimola Fruit Extract, Hydroxyethyl Urea, Niacinamide, Maltooligosyl Glucoside, Hydrogenated Starch Hydrolysate, Almond Oil Glycereth-8 Esters, Phenoxyethanol, Ethylhexylglycerin, Parfum, 1,2-Hexanediol, Centella Asiatica Leaf Vesicles, Nelumbo Nucifera Extract, Potassium Sorbate, Citric Acid, Trisodium Ethylenediamine Disuccinate, CI 45100.»

### 6. How to (`#how`, «Применение»)
- Grid 2 колонки (как About), `align-items:center`, padding `clamp(40px,6vw,88px) clamp(16px,4vw,56px)`.
- Колонка 1 (flex column gap 28): лейбл «Применение» (`margin-bottom:10px`), H2 «Умывание – это весело» (короткое тире «–», стиль как «Что внутри»). Список шагов — строки с `border-top:1px solid #F7C7DD` (у последней ещё `border-bottom`), `padding:18px 0`, gap 18, `align-items:baseline`; номер 13px/700/`#F52A82`, ширина 28px; текст `clamp(16px,1.4vw,19px)`/1.4:
  - 01 Выдави пенку на ладонь
  - 02 Распредели по влажной коже лица массажными движениями
  - 03 Смой тёплой водой
  
  Бейджи (flex, gap 10, wrap): «Не тестируется на животных», «Сертифицированная косметика» — `border:1px solid #151515`, `padding:8px 14px`, radius 999, 12px/500.
- Колонка 2: фото `photos/web/0929.jpg`, `aspect-ratio:4/5`, radius 16, cover.

### 7. UGC («Яркие эмоции»)
- Grid gap 20, padding как Benefits. Шапка: H2 «Яркие эмоции» + ссылка «@iffecta» (14px/500, `border-bottom:1.5px solid #151515`), space-between, `align-items:flex-end`.
- 4 фото в grid `minmax(min(100%,180px),1fr)`, gap 12, каждое `aspect-ratio:3/4`, radius 14, cover: `photos/web/0991.jpg`, `0787.jpg`, `1065.jpg`, `0883.jpg`. **Mobile:** строго 2 колонки.
- В прототипе блок скрывается пропом `showUgc` — в реализации сделать флагом в конфиге/CMS.

### 8. Lineup (`#lineup`, «Выбери своё настроение»)
- H2 «Выбери своё настроение». 3 карточки grid `minmax(min(100%,210px),1fr)`, gap 12.
- Карточка: radius 16, `overflow:hidden`, `position:relative`, flex column. Верх — фото `aspect-ratio:4/5`, фон под фото `#EDE9E4`, cover, `transition:transform .4s`. Низ — padding `20px 22px 24px`, flex column gap 8: строка space-between 11px/700/.1em/uppercase (название · «170 мл»), затем название активов `clamp(18px,1.6vw,22px)`/700/ls -.01em.
  1. фон `#C9EAF7` — `uploads/image (3).jpg` — «Розовая» · 170 мл — «Розовый лотос · экзосомы центеллы»
  2. фон `#F7C7DD` — `uploads/image (5).jpg` — «Жёлтая» · 170 мл — «Витамин С · экзосомы центеллы»
  3. фон `#D7C9EF` — `uploads/image (4).jpg` — «Синяя» · 170 мл — «Морские минералы · кокосовое молоко»
- **Hover (см. Interactions):** поверх фото появляется затемнение `rgba(21,21,21,.18)` и по центру кнопка «Купить» (→ `#buy`): фон `#F52A82`, белый, `padding:14px 28px`, radius 999, 15px/700, тень `0 10px 30px rgba(245,42,130,.35)`. Фото увеличивается до `scale(1.04)`.
- В прототипе блок скрывается пропом `showLineup`.

### 9. Buy (`#buy`, «Где купить»)
- Секция `position:relative`, `min-height:clamp(420px,60vh,620px)`, фон `#F7C7DD`. Фото `photos/web/1144.jpg` на всю секцию (cover).
- Оверлей с padding `clamp(16px,3vw,36px)`, flex, `align-items:flex-end; justify-content:flex-end`. Стеклянная карточка `width:min(360px,100%)`, `background:rgba(255,255,255,.6)`, `blur(16px)`, border как ранее, radius 16, padding 24, flex column gap 16; розовый кружок 28px в углу (18px). Лейбл «Где купить»; H2 «Подари себе моменты радости» (`clamp(26px,2.6vw,36px)`, 800, lh 1.05, ls -.03em, `#151515`); одна кнопка-строка «Купить на Wildberries» + «→» (space-between, фон `#151515`, белый, `padding:14px 18px`, radius 999, 14px/500; hover `#F52A82`). Ссылка — URL карточки WB (подставить).
- **Mobile:** фото становится обычным блоком высотой `clamp(300px,90vw,440px)`, карточка идёт под ним на всю ширину, padding секции 12px.

### 10. Footer
- Белая карточка radius 16. Верх: гигантская строка «Эмоции first!» `#F52A82`, 800, `font-size:14.2cqw` (контейнерные единицы; контейнер — `container-type:inline-size`), `line-height:.86`, `letter-spacing:-.05em`, `white-space:nowrap`, `margin:0 0 -.08em -.04em`, padding `clamp(28px,4vw,48px) clamp(16px,4vw,56px) 0`.
- Колонки grid `minmax(min(100%,200px),1fr)`, gap `clamp(24px,3vw,40px)`, padding `clamp(24px,3vw,40px) clamp(16px,4vw,56px)`, 13px/1.5:
  1. Логотип (высота 20px) + «Make cosmetics fun again» (`max-width:240px`).
  2. «Соцсети»: Instagram, TikTok, YouTube.
  3. «Где купить»: Wildberries, «Все пенки» (→ `#lineup`).
  4. «Документы»: Политика конфиденциальности, Пользовательское соглашение, Согласие на обработку персональных данных, Оферта — ведут на технические страницы (см. раздел 11).
  Заголовки колонок — лейбл-стиль `#F52A82`, `margin-bottom:4px`; ссылки 500.
- Низ: `border-top:1px solid #F7C7DD`, padding `16px … 20px`, 12px, цвет `#555`, space-between: «© 2026 IFFECTA. Все права защищены.» и `hello@iffecta.ru` (mailto).

### 11. Технические страницы (4 шт., один шаблон)
Файлы: `IFFECTA Политика конфиденциальности.dc.html`, `IFFECTA Пользовательское соглашение.dc.html`, `IFFECTA Согласие на обработку ПД.dc.html`, `IFFECTA Оферта.dc.html`. Реализовать как один компонент/шаблон `LegalPage` с данными (заголовок, вводный абзац, массив разделов).

**Структура (сверху вниз), та же обёртка, что у лендинга (фон `#F7C7DD`, белая карточка 1280 / radius 20):**
- **Header** — как на лендинге, но nav — 4 ссылки на документы (текущая — `#F52A82`), логотип ведёт на `/`, кнопка «Купить» → `/#buy`. **≤ 1100px:** nav скрыт.
- **Шапка документа** — padding `clamp(40px,6vw,88px) clamp(16px,4vw,56px) clamp(24px,3vw,40px)`, `border-bottom:1px solid #F7C7DD`, flex column gap 18: ссылка «← На главную» (13px/500); лейбл «Документы»; H1 `clamp(34px,5vw,72px)` / 800 / lh 1 / ls -.03em, `max-width` 12–18ch; два бейджа-пилюли (как в How to): «Редакция от 30.10.2026», «Действует с 30.10.2026» (даты — из данных).
- **Тело** — grid `280px minmax(0,1fr)`, gap `clamp(24px,4vw,56px)`, `align-items:start`, padding `clamp(28px,4vw,56px) clamp(16px,4vw,56px) clamp(40px,6vw,88px)`. **≤ 900px:** одна колонка, оглавление над текстом, не sticky.
  - **Оглавление** (`aside`): `position:sticky; top:24px`, фон `#F7C7DD`, radius 16, padding 22; лейбл «Содержание»; список якорных ссылок 14px/500/lh 1.35, gap 10, формат «1. Название».
  - **Текст** (`article`): `max-width:720px`, `clamp(15px,1.2vw,17px)` / lh 1.6, gap `clamp(28px,3vw,40px)`. Вводный абзац без номера. Каждый раздел: `padding-top:18px; border-top:1px solid #F7C7DD`, gap 12; H2 `clamp(20px,1.8vw,26px)` / 800 / lh 1.2 / ls -.02em с номером «01»… `#F52A82` и `margin-right:10px`; текст раздела `#555`. Последний раздел — реквизиты в карточке (`#F7C7DD`, radius 16, padding 22, 14px/1.5): «ЗАО «Вакуумные Ионные Технологии»» (700), «143502, Московская область, м.о. Истра, г. Истра, ул. Почтовая, д. 31, офис 206», «ОГРН 1025001820425 · ИНН 5017008889 · КПП 501701001», `hello@iffecta.ru` (`#F52A82`, 500).
- **Footer** — идентичен футеру лендинга (включая «Эмоции first!»); «Все пенки» → `/#lineup`.

**Содержание разделов.** Тексты в квадратных скобках `[…]` — заглушки-подсказки для юриста; в прод пойдут реальные тексты. Заголовки разделов и вводные абзацы — в HTML-файлах:
- Политика конфиденциальности — 10 разделов (Общие положения … Контакты оператора).
- Пользовательское соглашение — 10 разделов (Термины … Реквизиты и контакты).
- Согласие на обработку ПД — 8 разделов (Субъект и оператор … Контакты оператора).
- Публичная оферта — 10 разделов (Общие положения … Реквизиты продавца).

## Interactions & Behavior
- **Якорная навигация:** все «Купить»/«Хочу попробовать» ведут на `#buy`; nav — на секции. Плавный скролл приветствуется (`scroll-behavior:smooth`).
- **Ссылки:** `a` — `#151515`, без подчёркивания; hover — `#F52A82`.
- **Hero-видео поверх фото:** фото всегда рендерится. Видео: `muted loop playsinline preload=auto`, `opacity:0`. По событию `playing` → `opacity:1` (transition .6s). По `pause`/`error`/`stalled`/`waiting` → `opacity:0`. Источник: `hero-mobile.mp4` при `(max-width:640px)`, иначе `hero-desktop.mp4`; переключать по `matchMedia.change`. Если autoplay заблокирован — остаётся фото, ошибок не показывать.
- **Видео лотоса:** autoplay muted loop; в прототипе — страховочный `play()` по интервалу, в проде достаточно атрибутов.
- **Lineup hover:** `[card]:hover` / `:focus-within` → оверлей с кнопкой `opacity 0→1` (.25s ease), фото `scale(1.04)` (.4s ease). На тач-устройствах (`@media (hover:none)`) кнопка видна всегда.
- **Аккордеон «Полный состав»** — нативный `<details>`.
- **Кнопки hover:** чёрная → розовая, розовая → чёрная, outline → заливка (цвета выше). Transition не задан — можно `.2s ease`.
- Нет форм, нет состояний загрузки/ошибок.

## Responsive
- Лендинг: брейкпоинт один — **≤640px** — mobile. Всё остальное — fluid через `clamp()` и `auto-fit` гриды (две колонки появляются при ≥ ~624px контентной ширины).
- Технические страницы: **≤900px** — одна колонка (оглавление над текстом, не sticky); **≤1100px** — nav документов в шапке скрыт.
- Проверено на 390 / 768 / 1024 / 1440: без горизонтального скролла.
- Mobile-правила перечислены по секциям выше (hero 3:4, nav скрыт, текст About перед фото, фото Benefits 3:4, UGC 2 колонки, Buy стеком, CTA на всю ширину).
- Мин. размер тач-целей — кнопки ≥44px по высоте.

## State Management
- `heroVideoSrc` (derived от media query), `heroVideoVisible` (от событий видео).
- Опционально флаги `showUgc`, `showLineup` (bool, по умолчанию true).
- Данные статичны; CMS не требуется. Ссылка на WB — константа/env.

## Design Tokens
**Цвета**
- Розовый акцент `#F52A82` (CTA, заголовки, лейблы, маркеры)
- Фон страницы / мягкие карточки `#F7C7DD`
- Чёрный текст/кнопки `#151515`
- Белый `#FFFFFF`; второстепенный текст `#555555`
- Линейка: голубой `#C9EAF7`, сиреневый `#D7C9EF`, фон под флаконы `#EDE9E4`
- Стекло: `rgba(255,255,255,.55–.6)` + `blur(14–16px)` + `border 1px rgba(255,255,255,.7)`

**Шрифт** — Inter (Google Fonts), веса 400/500/700/800; fallback `system-ui, sans-serif`; `-webkit-font-smoothing:antialiased`.

**Типографика**
- Display H1: `clamp(44px,8.5vw,120px)` / 800 / lh .92 / ls -.04em
- H2 акцент (About): `clamp(40px,6.5vw,96px)` / 800 / lh .95 / ls -.04em
- H2 секций: `clamp(34px,4.5vw,64px)` / 800 / lh 1 / ls -.03em
- H3 лотос: `clamp(32px,4vw,56px)` / 800 / lh .98 / ls -.03em
- H2 Buy: `clamp(26px,2.6vw,36px)` / 800 / lh 1.05 / ls -.03em
- Лейбл: 11px / 700 / ls .12em / uppercase
- Карточные заголовки: 12px / 700 / ls .1em / uppercase
- Body L: `clamp(16px,1.4vw,19px)` / lh 1.4–1.45; Body M: `clamp(15px,1.3vw,18px)` / lh 1.5; Body S: 13–14px / lh 1.45–1.55; Nav/кнопки 14–15px / 500–700

**Радиусы** — основной контейнер 20px; секции/карточки 16px; стеклянные карточки 14–16px; картинки в составе 12px; UGC 14px; кнопки 999px.

**Тени** — CTA `0 10px 30px rgba(245,42,130,.3)`; стекло hero `0 10px 40px rgba(21,21,21,.08)`.

**Отступы** — секции `clamp(40px,6vw,88px)` по вертикали, `clamp(16px,4vw,56px)` по горизонтали; gap между колонками `clamp(24px,4vw,56px)`; gap карточек 12px; внешний паддинг страницы `clamp(12px,3vw,40px)`.

## Assets (в папке `assets/`)
- `brand/logo-oneline-black.png`, `brand/logo-oneline-white.png` — логотип.
- `photos/1028.jpg` hero; `0835.jpg` About; `1084.jpg` Benefits; `0929.jpg` How to; `0991.jpg`, `0787.jpg`, `1065.jpg`, `0883.jpg` UGC; `1144.jpg` Buy.
- `ingredients/centella.jpg`, `niacinamide.jpg`, `enzymes.jpg` — карточки состава.
- `lineup/pink.jpg`, `yellow.jpg`, `blue.jpg` — флаконы.
- `video/hero-desktop.mp4`, `video/hero-mobile.mp4` (1080×1920), `video/lotus.mp4`.
Все фото — собственные съёмки бренда. Для прода сжать (WebP/AVIF, srcset), видео — H.264 + faststart (уже сделано для hero-desktop).

## Files
- `IFFECTA Landing.dc.html` — основной прототип (desktop + mobile через media query).
- `IFFECTA Политика конфиденциальности.dc.html`, `IFFECTA Пользовательское соглашение.dc.html`, `IFFECTA Согласие на обработку ПД.dc.html`, `IFFECTA Оферта.dc.html` — технические страницы.
- `IFFECTA Landing Mobile.dc.html` — превью в рамке iPhone (только для просмотра).
- `support.js`, `image-slot.js`, `ios-frame.jsx` — рантайм прототипа, чтобы файлы открывались локально; в реализацию не переносить.
