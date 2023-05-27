import pandas as pd

# Read the .mca file
data = []

with open('data/input/Diamonds/MOnday/30lun1.mca', 'r', errors='ignore') as file:

    lines = file.readlines()[1:-1]
    start_index = lines.index('<<DATA>>\n') + 1
    end_index = lines.index('<<END>>\n')

    for line in lines[start_index:end_index]:
            value = int(line.strip())  # Convert the line to an integer
            data.append(value)  # Append the value to the list
   

# Extract the numerical data
print(data)

# Create a DataFrame from the data
df = pd.DataFrame(data, columns=['Value'])

# Print the DataFrame
print(df)