document.addEventListener('DOMContentLoaded', function () {
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalClose = document.getElementById('modal-close');

  if (!modalBackdrop) return;

  function openModal() {
    modalBackdrop.classList.remove('hidden');
  }

  function closeModal() {
    modalBackdrop.classList.add('hidden');
  }

  // If index.html provides loadPresentations() with auth checks, use it.
  const hasLoader = typeof window.loadPresentations === 'function';

  document.querySelectorAll('[data-modal="presentations"]').forEach(el => {
    el.addEventListener('click', async (e) => {
      e.preventDefault();
      if (hasLoader) {
        const ok = await window.loadPresentations();
        if (ok) openModal();
      } else {
        openModal();
      }
    });
  });

  if (modalClose) modalClose.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', function (e) {
    if (e.target === modalBackdrop) closeModal();
  });
});

/* Animated network background */
(function (){
  const canvas = document.getElementById('bg-network');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0, height = 0, dpr = Math.max(1, window.devicePixelRatio || 1);
  function resize(){
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }

  const cfg = {
    nodeCount: Math.max(18, Math.floor((window.innerWidth * window.innerHeight) / 90000)),
    maxLinkDist: 220,
    nodeRadius: 2.2,
    speed: 0.25,
    bgColorTop: 'rgba(6,24,48,0.0)',
    bgColorBottom: 'rgba(2,8,20,0.0)',
    nodeColor: 'rgba(180,230,255,0.95)',
    lineColor: 'rgba(180,230,255,0.12)'
  };

  let nodes = [];
  function initNodes(){
    nodes = [];
    for(let i=0;i<cfg.nodeCount;i++){
      nodes.push({
        x: Math.random()*width,
        y: Math.random()*height,
        vx: (Math.random()-0.5)*cfg.speed,
        vy: (Math.random()-0.5)*cfg.speed,
        r: cfg.nodeRadius + Math.random()*1.6
      });
    }
  }

  function step(){
    ctx.clearRect(0,0,width,height);

    // subtle gradient overlay (very transparent) to tint canvas
    const grad = ctx.createLinearGradient(0,0,0,height);
    grad.addColorStop(0, 'rgba(8,24,64,0.06)');
    grad.addColorStop(1, 'rgba(3,8,24,0.06)');
    ctx.fillStyle = grad;
    ctx.fillRect(0,0,width,height);

    // update nodes
    for(const n of nodes){
      n.x += n.vx;
      n.y += n.vy;
      if(n.x < -20) n.x = width + 20;
      if(n.x > width + 20) n.x = -20;
      if(n.y < -20) n.y = height + 20;
      if(n.y > height + 20) n.y = -20;
    }

    // draw links
    ctx.lineWidth = 1;
    for(let i=0;i<nodes.length;i++){
      const a = nodes[i];
      for(let j=i+1;j<nodes.length;j++){
        const b = nodes[j];
        const dx = a.x - b.x; const dy = a.y - b.y;
        const dist = Math.sqrt(dx*dx+dy*dy);
        if(dist < cfg.maxLinkDist){
          const alpha = 1 - (dist / cfg.maxLinkDist);
          ctx.strokeStyle = `rgba(180,230,255,${(alpha*0.12).toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    // draw nodes
    for(const n of nodes){
      ctx.beginPath();
      ctx.fillStyle = cfg.nodeColor;
      ctx.shadowColor = 'rgba(150,220,255,0.12)';
      ctx.shadowBlur = 14;
      ctx.arc(n.x, n.y, n.r, 0, Math.PI*2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    requestAnimationFrame(step);
  }

  // gentle resize + re-init
  function onResize(){
    resize();
    cfg.nodeCount = Math.max(18, Math.floor((window.innerWidth * window.innerHeight) / 90000));
    initNodes();
  }

  window.addEventListener('resize', onResize);
  resize(); initNodes(); requestAnimationFrame(step);
})();
