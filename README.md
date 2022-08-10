# Kaidun
A 3D game made in Python with moderngl

## **WHERE TO FIND THINGS**

- The project plan can be found at `TP2_ProjectPlan.md`
- The actual python file to run is `main.py`
- Files ending in `.test.py` are ordinary tests that use `assert`
- Files ending in `.vtest.py` show a function working visually
- Files ending in `.frag` or `.vert` contain GLSL shader code

## **WHAT IS IT DOING**

- Currently, it's following an edge on the graph and stopping at the end
- The rotation has a setpoint based on the heading of the edge, but you can still look around with the arrow keys
- You can also use o and p to adjust the third rotation axis
- Gravity has also been implemented, you can use the z key to jump

## **MODULES AND CREDIT**

Credit goes to the authors of the awesome modules:
- `numpy`, `moderngl`, `moderngl_window`
