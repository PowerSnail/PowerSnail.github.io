interface Point {
    x: number;
    y: number;
}

interface Rect {
    topLeft: Point;
    bottomRight: Point;
}

class PointSet {
    points: Map<number, Set<number>>;

    constructor() {
        this.points = new Map();
    }

    add(p: Point) {
        if (!this.points.has(p.x)) {
            this.points.set(p.x, new Set());
        }
        let row = this.points.get(p.x);
        if (row.has(p.y)) {
            return false;
        } else {
            row.add(p.y);
            return true;
        }
    }

    has(p: Point): boolean {
        return this.points.has(p.x) && this.points.get(p.x).has(p.y);
    }

    count(): number {
        let sum = 0;
        for (const s of this.points.values()) {
            sum += s.size;
        }
        return sum;
    }

    *[Symbol.iterator](): Iterator<Point> {
        for (const [x, s] of this.points.entries()) {
            for (const y of s) {
                yield { x: x, y: y };
            }
        }
    }
}

interface World {
    alive: PointSet;
    boundingBox: Rect;
}

function* neighbors(p: Point): IterableIterator<Point> {
    yield { x: p.x - 1, y: p.y - 1 };
    yield { x: p.x - 1, y: p.y };
    yield { x: p.x - 1, y: p.y + 1 };
    yield { x: p.x, y: p.y - 1 };
    yield { x: p.x, y: p.y + 1 };
    yield { x: p.x + 1, y: p.y - 1 };
    yield { x: p.x + 1, y: p.y };
    yield { x: p.x + 1, y: p.y + 1 };
}

function makeBoundingBox(points: Iterable<Point>, margin: number) {
    let boundingBox: Rect = {
        topLeft: { x: Infinity, y: Infinity },
        bottomRight: { x: -Infinity, y: -Infinity },
    };
    for (const p of points) {
        boundingBox.topLeft.x = Math.min(boundingBox.topLeft.x, p.x - margin);
        boundingBox.topLeft.y = Math.min(boundingBox.topLeft.y, p.y - margin);
        boundingBox.bottomRight.x = Math.max(
            boundingBox.bottomRight.x,
            p.x + margin
        );
        boundingBox.bottomRight.y = Math.max(
            boundingBox.bottomRight.y,
            p.y + margin
        );
    }
    return boundingBox;
}

function step(world: World): World {
    let potentially_alive: Map<number, Map<number, number>> = new Map();

    for (const p of world.alive) {
        for (const n of neighbors(p)) {
            if (!potentially_alive.has(n.x)) {
                potentially_alive.set(n.x, new Map());
            }
            let map_ref = potentially_alive.get(n.x);
            if (!map_ref.has(n.y)) {
                map_ref.set(n.y, 1);
            } else {
                map_ref.set(n.y, map_ref.get(n.y) + 1);
            }
        }
    }

    let alive: PointSet = new PointSet();
    for (const [x, row] of potentially_alive.entries()) {
        for (const [y, count] of row) {
            if (count == 3 || (count == 2 && world.alive.has({ x: x, y: y }))) {
                alive.add({ x: x, y: y });
            }
        }
    }

    return {
        alive: alive,
        boundingBox: makeBoundingBox(alive, 1),
    };
}

function getCenter(rect: Rect): Point {
    return {
        x: Math.floor((rect.topLeft.x + rect.bottomRight.x) / 2) || 0,
        y: Math.floor((rect.topLeft.y + rect.bottomRight.y) / 2) || 0,
    };
}

function render(world: World, context: CanvasRenderingContext2D) {
    let margin = 10;
    let unitPerRow = 100;
    let unitSize = Math.floor(
        (Math.min(context.canvas.width, context.canvas.height) - margin) /
        unitPerRow
    );

    // let center: Point = getCenter(world.boundingBox);
    let center: Point = { x: 0, y: 0 };
    let canvasRect: Rect = {
        topLeft: { x: 0, y: 0 },
        bottomRight: { x: context.canvas.width, y: context.canvas.height },
    };
    let canvasCenter: Point = getCenter(canvasRect);
    let offset: Point = {
        x: center.x * unitSize - canvasCenter.x,
        y: center.y * unitSize - canvasCenter.y,
    };

    context.imageSmoothingEnabled = true;
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);

    context.strokeStyle = "#fff";
    for (let x = center.x - unitPerRow / 2; x < center.x + unitPerRow / 2; x += 1) {
        for (let y = center.y - unitPerRow / 2; y < center.y + unitPerRow / 2; y += 1) {
            if (world.alive.has({ x: x, y: y })) {
                context.fillStyle = "#333";
            } else {
                context.fillStyle = "#ccc";
            }
            context.beginPath();
            context.rect(
                x * unitSize - offset.x,
                y * unitSize - offset.y,
                unitSize,
                unitSize
            );
            context.stroke();
            context.fill();
        }
    }

    if (world.alive.count() == 0) {
        context.fillStyle = "#00000044";
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);
        return;
    }
}

function initWorldWithBlinker(): World {
    let alive: PointSet = new PointSet();
    alive.add({ x: -1, y: 0 });
    alive.add({ x: 0, y: 0 });
    alive.add({ x: 1, y: 0 });

    return {
        alive: alive,
        boundingBox: makeBoundingBox(alive, 1),
    };
}

function initWorldRandomly(count_alive: number, range: Rect): World {
    let alive: PointSet = new PointSet();
    let width = range.bottomRight.x - range.topLeft.x;
    let height = range.bottomRight.y - range.topLeft.y;

    for (let n = 0; n < count_alive; n++) {
        while (
            !alive.add({
                x: Math.floor(Math.random() * width) + range.topLeft.x,
                y: Math.floor(Math.random() * height) + range.topLeft.y,
            })
        ) {
            // Nothing
        }
    }

    return {
        alive: alive, boundingBox: makeBoundingBox(alive, 1)
    }
}

function setupCanvas(canvas: HTMLCanvasElement) {
    // Get the device pixel ratio, falling back to 1.
    let dpr = window.devicePixelRatio || 1;
    // Get the size of the canvas in CSS pixels.
    let rect = canvas.getBoundingClientRect();
    // Give the canvas pixel dimensions of their CSS
    // size * the device pixel ratio.
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    let ctx = canvas.getContext("2d");
    // Scale all drawing operations by the dpr, so you
    // don't have to worry about the difference.
    ctx.scale(dpr, dpr);
    return ctx;
}

function runMainLoop() {
    let c = document.getElementById("mainCanvas") as HTMLCanvasElement;
    let context = setupCanvas(c);
    let world = initWorldRandomly(500, { topLeft: { x: -15, y: -15 }, bottomRight: { x: 15, y: 15 } });
    // let world = initWorldWithBlinker();
    render(world, context);

    let intervalId: number = null;

    function onTimeout() {
        world = step(world);
        render(world, context);
        if (world.alive.count() == 0) {
            clearInterval(intervalId);
        }
    }

    intervalId = setInterval(onTimeout, 100);
}

window.addEventListener("load", function () {
    runMainLoop();
});
