(function() {
    'use strict';

    // State
    let scrollY = 0;
    let targetScrollY = 0;
    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;
    let windowWidth = window.innerWidth;
    let windowHeight = window.innerHeight;
    let time = 0;

    // Elements
    const heroFloating = document.querySelectorAll('.floating-cv');
    const tunnelCvs = document.querySelectorAll('.tunnel-cv');
    const processTrack = document.querySelector('.process-track');
    const scrollScene = document.querySelector('.scroll-scene');
    const processScene = document.querySelector('.process-scene');

    function lerp(start, end, factor) {
        return start + (end - start) * factor;
    }

    function onMouseMove(e) {
        targetMouseX = (e.clientX / windowWidth - 0.5) * 2;
        targetMouseY = (e.clientY / windowHeight - 0.5) * 2;
    }

    function onScroll() {
        targetScrollY = window.scrollY;
    }

    function onResize() {
        windowWidth = window.innerWidth;
        windowHeight = window.innerHeight;
    }

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);

    function update() {
        time += 0.01;
        
        scrollY = lerp(scrollY, targetScrollY, 0.08);
        mouseX = lerp(mouseX, targetMouseX, 0.05);
        mouseY = lerp(mouseY, targetMouseY, 0.05);

        // 1. Hero Parallax & Tilt & Float
        heroFloating.forEach((el, index) => {
            const depth = (index + 1) * 15;
            // Float up and down
            const floatY = Math.sin(time + index * 2) * 20; 
            const floatX = Math.cos(time + index * 1.5) * 10;
            // Continuous gentle rotation
            const rotateAddX = Math.sin(time * 0.5 + index) * 10;
            const rotateAddY = Math.cos(time * 0.4 + index) * 15;
            
            const tiltX = mouseY * depth + rotateAddX;
            const tiltY = -mouseX * depth + rotateAddY;
            
            const moveX = mouseX * depth * 2 + floatX;
            const moveY = mouseY * depth * 2 + floatY;
            
            const baseZ = el.getAttribute('data-z') || 0;
            const rx = parseFloat(el.getAttribute('data-rx') || 0);
            const ry = parseFloat(el.getAttribute('data-ry') || 0);
            
            const finalRx = rx + tiltX;
            const finalRy = ry + tiltY;
            
            el.style.transform = 'translate3d(' + moveX + 'px, ' + moveY + 'px, ' + baseZ + 'px) rotateX(' + finalRx + 'deg) rotateY(' + finalRy + 'deg)';
        });

                // 2. Tunnel Auto-Scroll (Infinite Loop)
        if (scrollScene) {
            tunnelCvs.forEach((el, i) => {
                if (!el.hasAttribute('data-current-z')) {
                    el.setAttribute('data-current-z', el.getAttribute('data-z-offset'));
                }
                let currentZ = parseFloat(el.getAttribute('data-current-z'));
                // Move forward automatically
                currentZ += 8; // Speed of the tunnel
                if (currentZ > 1000) {
                    currentZ -= 4000; // Reset to the back seamlessly (8 templates * 500px spacing)
                }
                el.setAttribute('data-current-z', currentZ);
                
                // Fade out when close to camera, fade in when far
                const opacity = currentZ > 500 ? 1 - (currentZ-500)/500 : (currentZ < -3000 ? 1 - Math.abs(currentZ+3000)/1000 : 1);
                
                el.style.transform = 'translate(-50%, -50%) translateZ(' + currentZ + 'px)';
                el.style.opacity = Math.max(0, opacity);
            });
        }

        requestAnimationFrame(update);
    }

    update();
})();





