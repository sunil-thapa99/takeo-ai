Here is a detailed, step-by-step guide to complete your Azure Data Factory (ADF) Movie Analytics project, structured so you can easily take every required submission screenshot along the way.

---

## Phase 1: Database Setup & ADLS Gen2 Ingestion

### Step 1.1: Create Container and Upload File in ADLS Gen2

1. Log in to the **Azure Portal**.
2. Navigate to your **Storage Account** (ensure Hierarchical Namespace/ADLS Gen2 is enabled).
3. Under **Data storage**, select **Containers**.
4. Click **+ Container**, set the name to **`azure-project`**, and click **Create**.
5. Open the `azure-project` container and click **Upload**. Select your movie dataset CSV/Parquet file and upload it.

> 📸 **Screenshot 1 Required**: Azure Portal showing the `azure-project` container with the uploaded movie file inside.

---

### Step 1.2: Prepare Azure SQL Database Schema & Table

Run the following T-SQL script in **Azure Query Editor** or **SQL Server Management Studio (SSMS)** to create the required schema and table:

```sql
-- Create Schema
CREATE SCHEMA Test;
GO

-- Create Table with 2 columns
CREATE TABLE Test.generes (
    Genre VARCHAR(100),
    GenreCount INT
);
GO

```

---

## Phase 2: Create Linked Services & Datasets in ADF

Open **Azure Data Factory Studio** (`adf.azure.com`).

### Step 2.1: Create Linked Services

1. Go to the **Manage** tab (left sidebar) $\rightarrow$ **Linked services** $\rightarrow$ **+ New**.
2. **Linked Service 1 (ADLS Gen2)**:
* Select **Azure Data Lake Storage Gen2**.
* Name: `LS_ADLSGen2`
* Authentication type: *Account key* or *System-assigned Managed Identity*.
* Select your Azure Subscription and Storage Account.
* Click **Test Connection** $\rightarrow$ **Create**.


3. **Linked Service 2 (Azure SQL Database)**:
* Select **Azure SQL Database**.
* Name: `LS_AzureSQL`
* Select your Server Name, Database Name, and enter your credentials.
* Click **Test Connection** $\rightarrow$ **Create**.



> 📸 **Screenshot 2 Required**: The **Linked services** list page in ADF displaying both active linked services with a "Connection successful" state.

---

### Step 2.2: Create Datasets

1. Go to the **Author** tab $\rightarrow$ **Datasets** $\rightarrow$ **...** $\rightarrow$ **New dataset**.
2. **Dataset 1 (Source Movie Data)**:
* Choose **Azure Data Lake Storage Gen2** $\rightarrow$ Format (e.g., **DelimitedText** / CSV).
* Name: `ds_adls_movies`
* Linked Service: `LS_ADLSGen2`
* File path: Select `azure-project` container and choose your movie file.
* Check **First row as header**.


3. **Dataset 2 (Sink SQL Table)**:
* Choose **Azure SQL Database**.
* Name: `ds_sql_generes`
* Linked Service: `LS_AzureSQL`
* Table name: Select `[Test].[generes]`.



> 📸 **Screenshot 3 Required**: The ADF Authoring panel showing both `ds_adls_movies` and `ds_sql_generes` under Datasets.

---

## Phase 3: Build the Mapping Data Flow

1. In the **Author** tab, click **Data flows** $\rightarrow$ **...** $\rightarrow$ **New data flow**.
2. Turn ON **Data flow debug** at the top bar (allows you to preview output at each step).

```
[ Source: Movies Data ] 
          │
          ▼
[ Filter: Rating > 2 ]
          │
          ▼
[ Derived Column: Split Genres ]  <-- (If genres are delimited like "Action|Comedy")
          │
          ▼
[ Flatten: Unroll Genres ]         <-- (Produces 1 row per individual genre)
          │
          ▼
[ Aggregate: Count per Genre ]
          │
          ▼
[ Sink: Test.generes ]

```

### Detailed Transformation Settings:

#### 1. Source Node (`SourceMovies`)

* **Dataset**: `ds_adls_movies`

#### 2. Filter Node (`FilterRating`)

* **Incoming stream**: `SourceMovies`
* **Filter on**: `toDecimal(rating) > 2.0` *(or `toInteger(rating) > 2` depending on your column data type)*.

#### 3. Handling Multi-Genre Strings (Split & Flatten)

*(Most movie datasets store genres as delimited strings like `"Action|Adventure|Sci-Fi"`. If yours is already single-genre per row, skip to Step 5).*

* **Derived Column Node (`SplitGenres`)**:
* Column name: `GenreArray`
* Expression: `split(genres, '|')` *(Replace `'|'` with `','` if comma-separated)*.


* **Flatten Node (`FlattenGenres`)**:
* **Unroll by**: `GenreArray`
* **Input columns**: Map `GenreArray` to a new column `Genre`.



#### 4. Aggregate Node (`AggregateGenres`)

* **Group by**: `Genre`
* **Aggregates**:
* Column Name: `GenreCount`
* Expression: `count(1)`



#### 5. Sink Node (`SinkToAzureSQL`)

* **Incoming stream**: `AggregateGenres`
* **Dataset**: `ds_sql_generes`
* **Settings**: Set Table action to `Truncate table` (to ensure clean runs).

> 📸 **Screenshot 4 Required**: The completed **Data Flow canvas** showing the entire lineage flow from Source to Sink, along with a data preview at the Aggregate or Sink level.

---

## Phase 4: Create & Execute the ADF Pipeline

1. Go to **Author** $\rightarrow$ **Pipelines** $\rightarrow$ **...** $\rightarrow$ **New pipeline**.
2. Name: `pl_movies_analytics`.
3. Under **Activities**, expand **Move & transform**, then drag a **Data Flow** activity onto the canvas.
4. Select the Data Flow activity $\rightarrow$ **Settings** tab $\rightarrow$ Set **Data flow** to the Data Flow created in Phase 3.
5. Click **Publish all** to save your work.
6. Click **Add trigger** $\rightarrow$ **Trigger now** to run the pipeline.
7. Go to the **Monitor** tab (left sidebar) $\rightarrow$ **Pipeline runs** to check the status until it shows **Succeeded**.

> 📸 **Screenshot 5 Required**: The **Pipeline canvas** displaying the Data Flow activity AND/OR the **Monitor** tab showing the pipeline run status as **Succeeded**.

---

## Phase 5: Verification in Azure SQL Database

Run the following query in **Azure SQL Query Editor** or **SSMS** to verify the transformed output:

```sql
SELECT 
    Genre, 
    GenreCount 
FROM Test.generes 
ORDER BY GenreCount DESC;

```

> 📸 **Screenshot 6 Required**: Query output window in Azure SQL / SSMS showing the populated 2-column `Test.generes` table with unique genres and counts.

---

## Submission Checklist Summary

| # | Required Screenshot | Check |
| --- | --- | --- |
| 1 | Azure ADLS Gen2 `azure-project` container with uploaded file | [ ] |
| 2 | ADF Linked Services page showing ADLS Gen2 & Azure SQL connections | [ ] |
| 3 | ADF Datasets list showing source and sink datasets | [ ] |
| 4 | Mapping Data Flow graph showing transformations & Data Preview | [ ] |
| 5 | ADF Pipeline canvas & Monitor run status (Succeeded) | [ ] |
| 6 | Preview/Query output of `Test.generes` table in SQL DB | [ ] |