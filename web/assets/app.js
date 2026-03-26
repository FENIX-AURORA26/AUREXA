const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

const letters = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const fontSize = 14;
let columns = Math.floor(canvas.width / fontSize);
let drops = Array(columns).fill(1);

function draw() {
  ctx.fillStyle = 'rgba(6, 10, 18, 0.08)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#73f0c3';
  ctx.font = `${fontSize}px monospace`;

  for (let index = 0; index < drops.length; index += 1) {
    const text = letters[Math.floor(Math.random() * letters.length)];
    ctx.fillText(text, index * fontSize, drops[index] * fontSize);

    if (drops[index] * fontSize > canvas.height && Math.random() > 0.975) {
      drops[index] = 0;
    }
    drops[index] += 1;
  }
}

setInterval(() => {
  const nextColumns = Math.floor(canvas.width / fontSize);
  if (columns !== nextColumns) {
    columns = nextColumns;
    drops = Array(columns).fill(1);
  }
  draw();
}, 45);
