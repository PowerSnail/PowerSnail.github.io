function setupCanvas(canvas: HTMLCanvasElement) {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = +canvas.style.width * dpr;
    canvas.height = +canvas.style.height * dpr;
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    return ctx;
}

function clamp(v: number, min: number, max: number): number {
    return Math.min(max, Math.max(min, v));
}

class Dot {
    x: number = 0;
    y: number = 0;
    vx: number = 0.1;
    vy: number = 0.1;
    radius: number = 10;
    fill: string = "#FF0000";
    maxSpeed = 1;
    maxAcceleration = 0.1;

    render(context: CanvasRenderingContext2D) {
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        context.fillStyle = this.fill;
        context.fill();
    }

    step(elapsedTimeMS: number, width: number, height: number) {
        this.x += this.vx * elapsedTimeMS;
        this.y += this.vy * elapsedTimeMS;
        this.vx += (Math.random() - 0.5) * 2 * this.maxAcceleration;
        this.vy += (Math.random() - 0.5) * 2 * this.maxAcceleration;
        this.vx = clamp(this.vx, -this.maxSpeed, this.maxSpeed);
        this.vy = clamp(this.vy, -this.maxSpeed, this.maxSpeed);
        if (this.x >= width && this.vx > 0) {
            this.vx = - this.vx;
            this.x = width;
        }
        if (this.x < 0 && this.vx < 0) {
            this.vx = - this.vx;
            this.x = 0;
        }
        if (this.y >= height && this.vy > 0) {
            this.vy = - this.vy;
            this.y = height;
        }
        if (this.y < 0 && this.vy < 0) {
            this.vy = - this.vy;
            this.y = 0;
        }
    }
}

function runMainLoop() {
    const canvas = document.getElementById("mainCanvas") as HTMLCanvasElement;
    const inputRadius = document.getElementById("inputRadius") as HTMLInputElement;
    const inputColor = document.getElementById("inputColor") as HTMLInputElement;
    const inputSpeed = document.getElementById("inputSpeed") as HTMLInputElement;
    const inputAcceleration = document.getElementById("inputAcceleration") as HTMLInputElement;
    const buttonRestart = document.getElementById("buttonRestart") as HTMLButtonElement;
    const buttonStart = document.getElementById("buttonStart") as HTMLButtonElement;
    const buttonStop = document.getElementById("buttonStop") as HTMLButtonElement;
    const buttonFullscreen = document.getElementById("buttonFullscreen") as HTMLButtonElement;
    const context = setupCanvas(canvas);
    let dot = new Dot();
    let previousTime: number;

    const render = () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        dot.render(context);
    };

    const step = (timestamp: number) => {
        const rect = canvas.getBoundingClientRect();
        // const dpr = window.devicePixelRatio || 1;
        canvas.width = rect.width;
        canvas.height = rect.height;
        dot.step(timestamp - previousTime, canvas.clientWidth, canvas.clientHeight);
        if (buttonStop.disabled) {
            return;
        }
        previousTime = timestamp;
        render();
        requestAnimationFrame(step);
    }

    const continue_step = (timestamp: number) => {
        render();
        previousTime = timestamp;
        requestAnimationFrame(step);
    }

    const first_step = (timestamp: number) => {
        dot.x = 0;
        dot.y = 0;
        dot.vx = 0;
        dot.vy = 0;
        previousTime = timestamp;
        render();
        requestAnimationFrame(step);
    }

    inputRadius.valueAsNumber = dot.radius;
    inputColor.value = dot.fill;
    inputSpeed.valueAsNumber = dot.maxSpeed;
    inputAcceleration.valueAsNumber = dot.maxAcceleration;

    buttonRestart.onclick = (_) => {
        requestAnimationFrame(step);
        buttonStart.disabled = true;
        buttonStop.disabled = false;
        requestAnimationFrame(first_step);
    }
    buttonStart.onclick = (_) => {
        buttonStart.disabled = true;
        buttonStop.disabled = false;
        requestAnimationFrame(continue_step);
    }
    buttonStop.onclick = (_) => {
        buttonStart.disabled = false;
        buttonStop.disabled = true;
    }
    buttonFullscreen.onclick = (_) => {
        canvas.requestFullscreen();
    }

    inputRadius.oninput = (_) => { dot.radius = inputRadius.valueAsNumber; };
    inputColor.oninput = (_) => { dot.fill = inputColor.value; };
    inputSpeed.oninput = (_) => { dot.maxSpeed = inputSpeed.valueAsNumber; };
    inputAcceleration.oninput = (_) => { dot.maxAcceleration = inputAcceleration.valueAsNumber; };

    window.onresize = () => {
        const dpr = window.devicePixelRatio || 1;
        canvas.width = +canvas.style.width * dpr;
        canvas.height = +canvas.style.height * dpr;
    }

    requestAnimationFrame(first_step);
}

window.addEventListener("load", function () {
    runMainLoop();
});
