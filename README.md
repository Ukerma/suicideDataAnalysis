<h1>📊 Suicide Data Analysis by Country</h1>
<p>
   This project is a <strong>Suicide Data Analysis Tool</strong> created in Python. It allows users to analyze and visualize suicide data for a specific country. Statistical calculations, distribution tests, and visualizations are implemented to provide insights into the data trends and patterns.
</p>

<h2>🛠️ Features</h2>
<ul>
   <li> <strong>Country-Specific Analysis:</strong> Analyze suicide data for a selected country.</li>
   <li> <strong>Statistical Measures:</strong> Includes mean, median, mode, variance, standard deviation, skewness, and kurtosis calculations.</li>
   <li> <strong>Visualization:</strong> Provides detailed plots for yearly trends, gender comparison, age groups, GDP correlation, and generational analysis.</li>
   <li> <strong>Distribution Testing:</strong> Kolmogorov-Smirnov tests for normal, Poisson, and exponential distributions.</li>
   <li> <strong>Data Cleaning:</strong> GDP values are preprocessed and formatted for analysis.</li>
</ul>

<h2>⚙️ Technologies Used</h2>
<ul>
   <li> <strong>Language:</strong> Python</li>
   <li> <strong>Libraries:</strong> 
      <ul>
         <li><code>pandas</code>: For data manipulation and analysis.</li>
         <li><code>seaborn</code>: Advanced data visualization.</li>
         <li><code>matplotlib</code>: Plotting graphs and charts.</li>
         <li><code>numpy</code>: Numerical computations.</li>
         <li><code>scipy</code>: Statistical tests and analysis.</li>
      </ul>
   </li>
</ul>

<h2>🚀 How to Use</h2>
<ol>
   <li> Clone the repository and ensure the dataset (<code>master.csv</code>) is in the same directory as the script.</li>
   <li> Install the required libraries using pip:</li>
   <ul>
      <li><code>pip install pandas seaborn matplotlib numpy scipy</code></li>
   </ul>
   <li> Open the script and modify the <code>country</code> variable to the desired country.</li>
   <li> Run the script in your Python environment or terminal.</li>
   <li> View the statistical results and visualizations for the selected country in the console and as graphs.</li>
</ol>

<h2>💡 Example Outputs</h2>

<h3>📄 Console Output</h3>
<pre>
═══════════════════════════════════ General Information and Results ═══════════════════════════════════
Total Data Entries for Porto Rico: 300

═════════════ Porto Rico Suicide Rate Statistics (per 100K) ══════════════
Mean                : 8.75000
Median              : 6.50000
Mode                : 5.00000
Variance            : 4.23000
Standard Deviation  : 2.05600
Skewness            : 1.20400
Kurtosis            : -0.45600
</pre>

<h3>📊 Visualizations</h3>
<ul>
   <li>Yearly Trends: Total suicides over years plotted as a bar chart.</li>
   <li>Gender Comparison: Male vs. Female suicide counts as a line graph.</li>
   <li>GDP Correlation: GDP vs. suicide rates as a scatter plot.</li>
   <li>Age Group Analysis: Suicide rates by age group as line graphs.</li>
   <li>Generational Analysis: Suicide counts by generation as a bar chart.</li>
</ul>

<h2>👨‍💻 Authors</h2>
<p>
   This project was developed by <strong>Umut Kerim ACAR (ukerma)</strong> and <strong>Tuna DURUKAN (Laksy)</strong>.
</p>
