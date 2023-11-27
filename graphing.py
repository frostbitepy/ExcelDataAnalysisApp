import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

def claim_frequency_analysis(df):
    # Convert 'F/Emisión' to datetime if it's not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['F/Emisión']):
        df['F/Emisión'] = pd.to_datetime(df['F/Emisión'])
    
    # Set the style of seaborn for better visualization
    sns.set(style="whitegrid")

    # Function to format y-axis ticks as integers
    def format_ticks(value, _):
        return f'{int(value):,}'
    
    # Plot claim frequency by product
    plt.figure(figsize=(14, 8))
    sns.countplot(x='Nombre Producto', data=df, hue='Siniestro', palette="Set1")
    plt.title('Claim Frequency by Product')
    plt.xlabel('Product')
    plt.ylabel('Claim Count')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Claim')

    # Apply the custom tick formatter to the y-axis
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_ticks))

    # Show plot
    plt.show()

    # Plot claim frequency over time
    plt.figure(figsize=(14, 8))
    sns.countplot(x=df['F/Emisión'].dt.year, data=df, hue='Siniestro', palette="Set2")
    plt.title('Claim Frequency Over Time')
    plt.xlabel('Year of Issuance')
    plt.ylabel('Claim Count')
    plt.legend(title='Claim')

    # Apply the custom tick formatter to the y-axis
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_ticks))

    # Show plot
    plt.show()

    # Example of usage:
    # claim_frequency_analysis(your_dataframe)

def claim_severity_analysis_histogram(df):
    # Set the style of seaborn for better visualization
    sns.set(style="whitegrid")

    # Plot distribution of 'Suma Asegurada' by product using histograms
    plt.figure(figsize=(14, 8))
    for product in df['Nombre Producto'].unique():
        subset = df[df['Nombre Producto'] == product]
        plt.hist(subset['Suma Asegurada'], bins=20, alpha=0.5, label=product)

    plt.title('Distribution of Sum Insured by Product')
    plt.xlabel('Sum Insured')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    # Plot distribution of 'Prima' by product using histograms
    plt.figure(figsize=(14, 8))
    for product in df['Nombre Producto'].unique():
        subset = df[df['Nombre Producto'] == product]
        plt.hist(subset['Prima'], bins=20, alpha=0.5, label=product)

    plt.title('Distribution of Premium by Product')
    plt.xlabel('Premium')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    # Example of usage:
    # claim_severity_analysis_histogram(your_dataframe)

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def customer_segmentation(df):
    # Select relevant features for segmentation
    features_for_segmentation = ['Suma Asegurada', 'Prima', 'Cant. Stro.', 'Edad']

    # Subset the DataFrame with selected features
    subset_df = df[features_for_segmentation].copy()

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(subset_df)

    # Determine the optimal number of clusters using the Elbow method
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(scaled_features)
        wcss.append(kmeans.inertia_)

    # Plot the Elbow method
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
    plt.show()

    # Choose the optimal number of clusters based on the Elbow method (e.g., 3 clusters)
    optimal_clusters = 3

    # Perform K-Means clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    df['Cluster'] = kmeans.fit_predict(scaled_features)

    # Analyze the characteristics of high-risk segments
    cluster_analysis = df.groupby('Cluster')[features_for_segmentation].mean()

    # Print the cluster analysis
    print("Cluster Analysis:")
    print(cluster_analysis)

    # Visualize the clusters
    sns.pairplot(df, hue='Cluster', vars=features_for_segmentation, palette='Set1', diag_kind='kde')
    plt.suptitle('Customer Segmentation')
    plt.show()

    # Example of usage:
    # customer_segmentation(your_dataframe)