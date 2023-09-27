
# Generate the directory name and store it in a variable
dirname="../runs/run_$(date +%Y_%m_%d_%H_%M_%S)"

# Use the variable to create the directory
mkdir -p "$dirname"


cp -r initial_software "$dirname/software1"
cp -r initial_software "$dirname/software2"

cp name1.md "$dirname/software1/name.md"
cp name2.md "$dirname/software2/name.md"


cp specific_goal_1.md "$dirname/software1/specific_goal.md"
cp specific_goal_2.md "$dirname/software2/specific_goal.md"


podman run \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -v "$dirname/software1":/app/env1/software \
    -v "$dirname/software2":/app/env2/software \
    -w /app \
    evolver:latest python3 loop.py
