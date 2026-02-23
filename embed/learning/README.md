# Embeddings Learning Activity

**Goal**: Help students understand vector embeddings through interactive exploration and visualization

## Learning Objectives

1. Understand what embeddings are and how they represent semantic meaning
2. Explore embedding arithmetic (e.g., "King" - "Man" + "Woman" ≈ "Queen")
3. Visualize high-dimensional vectors in an intuitive way
4. Build intuition for similarity and distance in embedding space

## Activity Overview

Students will:
1. Embed a curated set of words using OpenAI's embedding API
2. Perform vector arithmetic to discover semantic relationships
3. Visualize embeddings using color-coded dimension bars
4. Experiment with their own words and relationships

## Suggested Word Sets

### Gender & Royalty
- King, Queen, Man, Woman, Prince, Princess

### Geography & Capitals
- France, Paris, Germany, Berlin, Italy, Rome

### Comparatives
- Big, Bigger, Biggest, Small, Smaller, Smallest

### Opposites
- Hot, Cold, Happy, Sad, Fast, Slow, Light, Dark

### Professions
- Doctor, Nurse, Teacher, Student, Chef, Cook

### Animals & Sounds
- Dog, Bark, Cat, Meow, Cow, Moo

## Embedding Arithmetic Examples

### Classic Analogy
```
King - Man + Woman ≈ Queen
```

### Capital Cities
```
France - Paris + Berlin ≈ Germany
```

### Comparatives
```
Big + (Bigger - Big) ≈ Bigger
```

## Visualization Approach

### Color-Coded Dimension Bars

Each word is represented as a horizontal bar chart where:
- Each dimension (1-1536 for text-embedding-3-small) is assigned a color
- Bar width/intensity represents the value in that dimension
- Similar words should have similar color patterns

**Example visualization:**
```
King:    [████████░░░░░░░░████░░░░████████░░░░...]
Queen:   [████████░░░░░░░░░░░░████████████░░░░...]
Man:     [████████░░░░░░░░░░░░░░░░████░░░░░░░░...]
Woman:   [████████░░░░░░░░░░░░░░░░████████░░░░...]
```

### Alternative Visualizations
- **t-SNE/UMAP**: Reduce to 2D for scatter plot
- **Heatmap**: Show dimension values as color intensity
- **Similarity Matrix**: Pairwise cosine similarity between all words
- **3D Plot**: Interactive 3D visualization using PCA

## Technical Implementation

### Tools & Libraries
- **OpenAI API**: Generate embeddings
- **NumPy**: Vector arithmetic
- **Matplotlib/Plotly**: Visualization
- **scikit-learn**: Dimensionality reduction (t-SNE, PCA)

### Key Functions
```python
def embed_word(word):
    """Generate embedding for a single word"""
    
def vector_arithmetic(word1, word2, word3):
    """Compute: word1 - word2 + word3"""
    
def find_closest(target_vector, word_embeddings):
    """Find most similar word to target vector"""
    
def visualize_dimensions(word_embeddings):
    """Create color-coded dimension bars"""
    
def cosine_similarity(vec1, vec2):
    """Compute similarity between two vectors"""
```

## Interactive Elements

### Web Interface
- Input field to add custom words
- Dropdown to select arithmetic operations
- Real-time visualization updates
- Similarity score display

### Jupyter Notebook
- Step-by-step guided exploration
- Code cells for experimentation
- Interactive widgets (ipywidgets)
- Markdown explanations

## Deliverables

1. **Interactive Web App** (`embeddings-explorer/`)
   - Next.js or React app
   - OpenAI API integration
   - Real-time visualization

2. **Jupyter Notebook** (`embeddings_activity.ipynb`)
   - Google Colab compatible
   - Pre-loaded examples
   - Exercises for students

3. **Python Library** (`embedding_viz.py`)
   - Reusable visualization functions
   - Easy to integrate into other projects

## Success Criteria

✅ Students can embed words and see vector representations
✅ Vector arithmetic produces semantically meaningful results
✅ Visualizations are intuitive and educational
✅ Students can experiment with their own word sets
✅ Clear connection to RAG and similarity search concepts
