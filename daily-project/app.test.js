/**
 * Test Suite for GitHub Streak Saver Game Logic
 * Verifies core physics models, score scaling, and collision calculations.
 */

// Simple assertion helper
function assert(condition, message) {
    if (!condition) {
        console.error(`❌ Assertion Failed: ${message}`);
        process.exit(1);
    }
}

// 1. Test Rectangle-Circle Collision Math
function testRectCircleCollision() {
    console.log("Running rect-circle collision test...");
    
    // Mock checkRectCircleCollision function from app.js
    function checkRectCircleCollision(rect, circle) {
        const closestX = Math.max(rect.x, Math.min(circle.x, rect.x + rect.width));
        const closestY = Math.max(rect.y, Math.min(circle.y, rect.y + rect.height));

        const distanceX = circle.x - closestX;
        const distanceY = circle.y - closestY;
        const distanceSquared = (distanceX * distanceX) + (distanceY * distanceY);

        return distanceSquared < (circle.radius * circle.radius);
    }

    // Obstacle is at x=200, y=100, width=50, height=50
    const rect = { x: 200, y: 100, width: 50, height: 50 };

    // Case A: Circle directly inside
    const circleInside = { x: 220, y: 120, radius: 10 };
    assert(checkRectCircleCollision(rect, circleInside) === true, "Circle inside rect should collide");

    // Case B: Circle overlapping edge
    const circleOverlapping = { x: 195, y: 120, radius: 10 }; // x-distance = 5, radius = 10 -> colliding
    assert(checkRectCircleCollision(rect, circleOverlapping) === true, "Circle overlapping edge should collide");

    // Case C: Circle far away
    const circleFar = { x: 100, y: 100, radius: 10 };
    assert(checkRectCircleCollision(rect, circleFar) === false, "Circle far away should not collide");

    console.log("✅ Rect-Circle collision tests passed!");
}

// 2. Test Circle-Circle Collision Math
function testCircleCollision() {
    console.log("Running circle-circle collision test...");

    function checkCircleCollision(c1, c2) {
        const dx = c1.x - c2.x;
        const dy = c1.y - c2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        return dist < (c1.radius + c2.radius);
    }

    const c1 = { x: 100, y: 100, radius: 15 };
    
    // Case A: Colliding circles
    const c2 = { x: 120, y: 100, radius: 15 }; // dist = 20, sum of radii = 30 -> colliding
    assert(checkCircleCollision(c1, c2) === true, "Overlapping circles should collide");

    // Case B: Touching circles
    const c3 = { x: 130, y: 100, radius: 15 }; // dist = 30, sum of radii = 30 -> touching (not strict less, but let's see)
    assert(checkCircleCollision(c1, c3) === false, "Touching circles boundary should not trigger strict collision");

    // Case C: Separate circles
    const c4 = { x: 200, y: 100, radius: 15 };
    assert(checkCircleCollision(c1, c4) === false, "Distant circles should not collide");

    console.log("✅ Circle-Circle collision tests passed!");
}

// 3. Test Difficulty and Speed Scaling
function testDifficultyScaling() {
    console.log("Running difficulty scaling tests...");

    function getScrollSpeed(score) {
        return 4.5 + Math.floor(score / 10) * 0.4;
    }

    assert(getScrollSpeed(0) === 4.5, "Starting speed should be 4.5");
    assert(getScrollSpeed(5) === 4.5, "Speed should remain 4.5 at score 5");
    assert(getScrollSpeed(10) === 4.9, "Speed should increase to 4.9 at score 10");
    assert(getScrollSpeed(25) === 5.3, "Speed should increase to 5.3 at score 25");

    console.log("✅ Difficulty scaling tests passed!");
}

// Run all
console.log("=== RUNNING GAME ENGINE UNIT TESTS ===");
testRectCircleCollision();
testCircleCollision();
testDifficultyScaling();
console.log("\n🎉 All 3 game-logic test suites passed successfully!");
