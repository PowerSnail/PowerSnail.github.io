# Particle

A particle is a point with position and velocity. It may have other properties, like color, size, etc.

$$p += v \cdot dt$$
$$v += a \cdot dt$$

## Fireworks

Particles are given a large initial velocity. When it reaches a height, it shoots out more particles with large initial velocity.

## Billboarding

Find the particle, draw a rectangle at the point with a texture.

## Fire Simulation

- Particles scattering
- Strong upward accelerating
- Translucent, streak, rectangular billboards

## Cloud

- Scattering at all different velocities/directions
- Rapid slow down
- Almost transparent billboards, adding up to almost opaque cloud

## Sand

- Particles that are rough
    - bumpy
    - non-spherical

But we assume these particles are sphere.

### Bouncing

1. hitting ground (a plane)

- Surface Normal
- Force division:
    + parallel to surface normal: surface giving upwards force
    + perpendicular to surface normal: downward motion force component
    + new velocity: composing the two forces above

2. Sand-sand collision

- Two spheres collide:
    + original momentum
    + constraints (forces)
    + conservation of momentum
    + kinetic energy consumed by friction
    + Solve a non-linear system of equation

We collect all the contraints and solve the system. This is called non-local simulation. The system is very hard to solve, because a particle can be affected by any particle at arbitrarily far distance.


In local simulation, we solve the collision by only care about the constraints between each pair of touching particle. This is less correct but more efficient.

Certain ordering is better, for example, working from ground upwards.

The problem is that particles could overlap, because the constraints are non-local and thus not realistic. Then we need to add constraints such as when they overlap, they bounce off.


# Water

- Round
- Cluster

Particle Simulations:

- Water particles tend to maintain a certain number of neighbors at certain distance (density)
- At the boundary, there are less neighbors, and thus it tends to pull closer to other particles

## Smooth Particles

Each particle has

- x, y, z
- velocity
- density
- temperature
- etc.

The influence of a particle fade as distance increases. Within the maximum range of influence, find all the particles and calculate the sum of influence on the target particle.

$$
\begin{align*}
    p &+= v \cdot dt \\
    v &+= a \cdot dt \\
    a &= \dfrac{F}{m} \\
    F &= g + \text{collision} + \text{density correction}
\end{align*}
$$

## Water Appearance: Marching Cube

Find the boundary of water using marching cubes, and use ray tracing to render the water.

## Parameters of Fluid Simulation

1. Particle size
     - high frequency dynamic requires smal particle size.
     - large size leads to larger minimum features, which will make the fluid thicker
     - small size leads to more computation: $\text{# of particle} \propto \dfrac{\text{volume}}{\text{particle size}^3}$

2. Viscosity
     - More Viscosity leads to thicker fluid
     - The less viscosity, the harder for features to appear

3. Elasticity

If two particles are close together, there is a spring between them. It tends to maintain its original shape.

Elasto-viscous fluid: High viscosity and elasticity, like jello.

- folding onto itself when pouring

