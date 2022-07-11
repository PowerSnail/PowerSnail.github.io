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
        let row = get_or_insert(this.points, p.x, () => new Set())
        if (row.has(p.y)) {
            return false;
        } else {
            row.add(p.y);
            return true;
        }
    }

    has(p: Point): boolean {
        let row = this.points.get(p.x);
        return (row !== undefined) && row.has(p.y);
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
    width: number;
    height: number;
}

function* neighbors(w: World, p: Point): IterableIterator<Point> {
    yield { x: (p.x - 1 + w.width) % w.width, y: (p.y - 1 + w.height) % w.height };
    yield { x: (p.x - 1 + w.width) % w.width, y: (p.y + w.height) % w.height };
    yield { x: (p.x - 1 + w.width) % w.width, y: (p.y + 1 + w.height) % w.height };
    yield { x: (p.x + w.width) % w.width, y: (p.y - 1 + w.height) % w.height };
    yield { x: (p.x + w.width) % w.width, y: (p.y + 1 + w.height) % w.height };
    yield { x: (p.x + 1 + w.width) % w.width, y: (p.y - 1 + w.height) % w.height };
    yield { x: (p.x + 1 + w.width) % w.width, y: (p.y + w.height) % w.height };
    yield { x: (p.x + 1 + w.width) % w.width, y: (p.y + 1 + w.height) % w.height };
}

function get_or_insert<K, V>(map: Map<K, V>, key: K, default_v: () => V): V {
    let value = map.get(key);
    if (value === undefined) {
        let v = default_v()
        map.set(key, v);
        return v;
    } else {
        return value;
    }
}

function step(world: World): World {
    let number_of_neighbor: Map<number, Map<number, number>> = new Map();

    for (const p of world.alive) {
        for (const n of neighbors(world, p)) {
            let map_ref = get_or_insert(number_of_neighbor, n.x, () => new Map())
            let old_count = get_or_insert(map_ref, n.y, () => 0);
            map_ref.set(n.y, old_count + 1)
        }
    }

    let alive: PointSet = new PointSet();
    for (const [x, row] of number_of_neighbor.entries()) {
        for (const [y, count] of row) {
            if (count == 3 || (count == 2 && world.alive.has({ x: x, y: y }))) {
                alive.add({ x: x, y: y });
            }
        }
    }

    return {
        alive: alive,
        width: world.width,
        height: world.height,
    };
}

function render(world: World, canvas: HTMLCanvasElement) {
    let dpr = window.devicePixelRatio || 1;
    let rect = canvas.getBoundingClientRect();
    let context = canvas.getContext("2d")! as CanvasRenderingContext2D;

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;

    let margin = 10;
    let unitSize = (canvas.width - margin * 2) / world.width;

    context.imageSmoothingEnabled = false;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "#eee";
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.strokeStyle = "#fff";
    for (let x = 0; x < world.width; x += 1) {
        for (let y = 0; y < world.height; y += 1) {
            if (world.alive.has({ x: x, y: y })) {
                context.fillStyle = "#333";
            } else {
                context.fillStyle = "#ccc";
            }
            context.fillRect(
                x * unitSize + margin,
                y * unitSize + margin,
                unitSize - 1,
                unitSize - 1
            );
        }
    }

    if (world.alive.count() == 0) {
        context.fillStyle = "#00000044";
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);
        return;
    }
}

function initWorldWithBlinker(width: number, height: number): World {
    let alive: PointSet = new PointSet();
    alive.add({ x: -1, y: 0 });
    alive.add({ x: 0, y: 0 });
    alive.add({ x: 1, y: 0 });

    return {
        alive: alive,
        width: width,
        height: height
    };
}

function initWorldRandomly(count_alive: number, width: number, height: number): World {
    let alive: PointSet = new PointSet();

    for (let n = 0; n < count_alive; n++) {
        while (
            !alive.add({
                x: Math.floor(Math.random() * width),
                y: Math.floor(Math.random() * height),
            })
        ) {
            // Nothing
        }
    }

    return {
        alive: alive,
        width: width,
        height: height
    }
}

function runMainLoop() {
    let c = document.getElementById("mainCanvas") as HTMLCanvasElement;

    let world = initWorldRandomly(100 * 100 / 3, 100, 100);
    // let world = initWorldWithBlinker();
    render(world, c);

    let intervalId: number = 0;

    function onTimeout() {
        world = step(world);
        render(world, c);
        if (world.alive.count() == 0) {
            clearInterval(intervalId);
        }
    }

    intervalId = setInterval(onTimeout, 100);
}

window.addEventListener("load", function () {
    runMainLoop();
});
