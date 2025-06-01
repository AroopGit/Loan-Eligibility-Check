# Credit Approval System

A Django-based backend system for processing credit approvals, checking loan eligibility, and managing loan applications.

## Features

- Customer registration with automatic credit limit calculation
- Loan eligibility checks based on credit scoring
- Loan creation and management
- API endpoints for viewing loan details
- Background data ingestion from Excel files

## Project Setup

### Prerequisites

- Docker and Docker Compose

### Running the Application

1. Clone the repository
2. Add the data files to the `data` directory:
   - `customer_data.xlsx`
   - `loan_data.xlsx`
3. Run the application with Docker Compose:

```bash
docker-compose up
```

The API will be available at http://localhost:8000/api/

## API Endpoints

### 1. Register Customer

```
POST /api/register
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}
```

### 2. Check Loan Eligibility

```
POST /api/check-eligibility
```

**Request Body:**
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 12.5,
  "tenure": 12
}
```

### 3. Create Loan

```
POST /api/create-loan
```

**Request Body:**
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 12.5,
  "tenure": 12
}
```

### 4. View Loan Details

```
GET /api/view-loan/{loan_id}
```

### 5. View Customer Loans

```
GET /api/view-loans/{customer_id}
```

## Technical Details

The application implements the following key features:

1. **Credit Scoring Algorithm**: Calculates a credit score based on past loan history, current debt, and financial status
2. **Interest Rate Adjustment**: Adjusts interest rates based on credit score
3. **Monthly Installment Calculation**: Uses compound interest formula for calculating EMIs
4. **Background Data Processing**: Uses Celery for background processing of initial data
5. **Comprehensive API**: Provides a complete set of endpoints for loan management

The system is fully containerized with Docker and uses PostgreSQL for data storage and Redis for background task messaging.
