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

    constructor () {
        this.points = new Map();
    }

    add(p: Point) {
        if (!this.points.has(p.x)) {
            this.points.set(p.x, new Set());
        }
        this.points.get(p.x).add(p.y);
    }

    has(p: Point): boolean {
        return this.points.has(p.x) && this.points.get(p.x).has(p.y);
    }

    *[Symbol.iterator](): Iterator<Point> {
        for (const [x, s] of this.points.entries()) {
            for (const y of s) {
                yield { x: x, y: y }
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
    let boundingBox: Rect = { topLeft: { x: Infinity, y: Infinity }, bottomRight: { x: -Infinity, y: -Infinity } };
    for (const p of points) {
        boundingBox.topLeft.x = Math.min(boundingBox.topLeft.x, p.x - margin);
        boundingBox.topLeft.y = Math.min(boundingBox.topLeft.y, p.y - margin);
        boundingBox.bottomRight.x = Math.max(boundingBox.bottomRight.x, p.x + margin);
        boundingBox.bottomRight.y = Math.max(boundingBox.bottomRight.y, p.y + margin);
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
    };

    let alive: PointSet = new PointSet;
    for (const [x, row] of potentially_alive.entries()) {
        for (const [y, count] of row) {
            if (count == 3 || (count == 2 && world.alive.has({x: x, y: y}))) {
                alive.add({x: x, y: y});
            }
        }
    }

    return {
        alive: alive, boundingBox: makeBoundingBox(alive, 1)
    };
}

function render(world: World, canvas: HTMLCanvasElement) {
    let center: Point = {
        x: Math.floor((world.boundingBox.topLeft.x + world.boundingBox.bottomRight.x) / 2),
        y: Math.floor((world.boundingBox.topLeft.y + world.boundingBox.bottomRight.y) / 2),
    };
    let renderBox: Rect = {
        topLeft: { x: center.x - 40, y: center.y - 40 },
        bottomRight: { x: center.x + 40, y: center.y + 40 },
    };

    let unitSize = Math.min(canvas.width, canvas.height) / 200;
    let offset: Point = { x: renderBox.topLeft.x * unitSize, y: renderBox.topLeft.y * unitSize };
    let context = canvas.getContext("2d")
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (const p of world.alive) {
        context.fillRect(p.x * unitSize - offset.x, p.y * unitSize - offset.y, unitSize, unitSize);
    }
}


function initialize_with_blinker(): World {
    let alive: PointSet = new PointSet;
    alive.add({ x: -1, y: 0 });
    alive.add({ x: 0, y: 0 });
    alive.add({ x: 1, y: 0 });

    return {
        alive: alive,
        boundingBox: makeBoundingBox(alive, 1),
    }
}


let c = document.getElementById("mainCanvas") as HTMLCanvasElement;
let world = initialize_with_blinker();
render(world, c);

function onTimeout() {
    world = step(world);
    render(world, c);
}

setInterval(onTimeout, 1000);


// let alive: Set<Point> = new Set();
// let a = alive.add({ x: -1, y: 0 });
// a = alive.add({ x: 0, y: 0 });
// a = alive.add({ x: 1, y: 0 });
// a = alive.add({ x: 1, y: 0 });
// a = alive.add({ x: 1, y: 0 });
// a = alive.add({ x: 3, y: 0 });
// a = alive.add({ x: 4, y: 0 });

// console.log(a)
// for (const n of alive) {
//     console.log(JSON.stringify(n));
// }

// console.log("123")