# Handoff: IFFECTA — страница 404

## Overview
Страница ошибки 404 для сайта IFFECTA. Сообщает, что адреса нет, и возвращает пользователя на главную или к покупке. Визуально — продолжение лендинга (та же шапка, цвета, типографика, стеклянная плашка).

## About the Design Files
`IFFECTA 404.dc.html` — **дизайн-референс в HTML**, прототип внешнего вида и поведения, не продакшн-код. Задача — воссоздать страницу в стеке проекта, где уже реализован лендинг (общий `Header`, кнопки, плашка — переиспользовать). Разметка внутри `<x-dc>…</x-dc>`, стили инлайновые; `style-hover="…"` — hover-состояние; `data-m-*` — метки элементов для мобильных правил из `@media (max-width:640px)` в `<style>`. `support.js` — рантайм прототипа, не переносить.

## Fidelity
**High-fidelity.** Цвета, типографика, отступы и тексты финальные.

## Layout
Фон страницы `#F7C7DD`, внешний паддинг `clamp(12px,3vw,40px)`; страница — flex column на `min-height:100vh`, белая карточка растягивается (`flex:1`) до футера.

### 1. Header (идентичен лендингу)
flex, space-between, `padding:6px 4px 22px`, `max-width:1280px`. Логотип `logo-oneline-black.png` h=22px → `/`. Nav 14px/500: «О пенке» `/#about`, «Состав» `/#actives`, «Применение» `/#how`, «Линейка» `/#lineup`. Кнопка «Купить» → `/#buy`: `#151515`/`#fff`, `padding:10px 18px`, radius 999, 14px/500; hover `#F52A82`. **Mobile:** nav скрыт.

### 2. Основная карточка
`max-width:1280px`, белая, radius 20, `overflow:hidden`. Grid `repeat(auto-fit, minmax(min(100%,320px),1fr))`, `align-items:stretch` — две равные колонки на desktop, стек на mobile (текст сверху, фото снизу).

**Левая колонка** — padding `clamp(32px,5vw,72px) clamp(20px,4vw,56px)`, flex column, `justify-content:space-between`, gap 40:
- Лейбл «Ошибка 404» — 11px/700, `letter-spacing:.12em`, uppercase, `#F52A82`.
- Цифры «404» — `clamp(96px,16vw,240px)`, 800, `line-height:.85`, `letter-spacing:-.06em`, `#F52A82`.
- H1 «Эта страница смылась.» — `clamp(28px,3.2vw,44px)`, 800, lh 1.05, ls -.03em, `#151515`, `max-width:16ch`.
- Абзац «Такого адреса нет или он изменился. Но пенка на месте — возвращайся на главную.» — `clamp(15px,1.3vw,18px)`, lh 1.5, `max-width:420px`.
- Кнопки (flex, gap 10, wrap), прижаты к низу колонки:
  - «На главную» → `/`: фон `#F52A82`, белый, `padding:16px 28px`, radius 999, 15px/700, ls -.01em, тень `0 10px 30px rgba(245,42,130,.3)`; hover фон `#151515`.
  - «Купить пенку» → `/#buy`: `border:1.5px solid #F52A82`, текст `#F52A82`, `padding:14px 22px`, radius 999, 14px/500; hover — заливка `#F52A82`, текст белый.
  - **Mobile:** обе кнопки на всю ширину, текст по центру.

**Правая колонка** — `position:relative`, `min-height:clamp(420px,60vh,720px)`, `overflow:hidden`. Фото `0929.jpg`, `object-fit:cover`, `object-position:50% 20%`. **Mobile:** `aspect-ratio:4/5`, min-height снимается.
- Стеклянная плашка в левом нижнем углу (offset `clamp(16px,3vw,32px)`), `width:min(280px, calc(100% - 32px))`: `background:rgba(255,255,255,.55)`, `backdrop-filter:blur(14px)`, `border:1px solid rgba(255,255,255,.7)`, radius 14, `padding:18px 18px 20px`; розовый кружок 28px `#F52A82` в правом верхнем углу (top/right 14px); лейбл «Эмоции first!» (11px/700/.12em/uppercase/`#F52A82`, `margin-bottom:8px`); текст «Даже на 404 можно улыбнуться.» 13px/1.45.

### 3. Footer (короткий)
Белая карточка radius 16, `margin-top:16px`, padding `16px clamp(16px,4vw,56px) 20px`, flex space-between, 12px, `#555`: «© 2026 IFFECTA. Все права защищены.» и `hello@iffecta.ru` (mailto).

## Interactions & Behavior
- Отдавать с HTTP-статусом **404**.
- Ссылки: `#151515`, hover `#F52A82`; кнопки — hover-цвета выше (transition `.2s ease` допустим).
- Анимаций нет. Состояний загрузки/ошибок нет.

## Responsive
Один брейкпоинт **≤640px**: nav скрыт, колонки стеком (текст → фото), кнопки full-width, фото 4:5. Всё остальное fluid через `clamp()`.

## Design Tokens
- Цвета: акцент `#F52A82`; фон `#F7C7DD`; текст/кнопка `#151515`; белый `#FFFFFF`; вторичный `#555555`; стекло `rgba(255,255,255,.55)` + `blur(14px)` + border `rgba(255,255,255,.7)`.
- Шрифт: Inter (Google Fonts) 400/500/700/800, fallback `system-ui, sans-serif`.
- Радиусы: карточка 20, футер 16, плашка 14, кнопки 999.
- Тень CTA: `0 10px 30px rgba(245,42,130,.3)`.

## Assets (`assets/`)
- `brand/logo-oneline-black.png` — логотип.
- `photos/0929.jpg` — фото (ладонь с пеной). Собственная съёмка бренда; для прода — WebP/AVIF + srcset.

## Files
- `IFFECTA 404.dc.html` — прототип.
- `support.js` — рантайм прототипа, чтобы файл открывался локально; не переносить.
