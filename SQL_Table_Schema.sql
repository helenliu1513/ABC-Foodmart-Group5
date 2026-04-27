-- APAN5310 Project Checkpoint 3 Group 5

CREATE TABLE store (
    store_id        INTEGER,
    store_name      VARCHAR(100) NOT NULL,
    borough         VARCHAR(50),
    street_address  VARCHAR(200),
    phone_number    VARCHAR(20),
    open_date       DATE,
    store_status    VARCHAR(20),
    PRIMARY KEY (store_id),
    CHECK (store_status IN ('Open', 'Closed', 'Renovation'))
);

CREATE TABLE department (
    department_id           INTEGER,
    department_name         VARCHAR(100) NOT NULL,
    department_description  VARCHAR(255),
    PRIMARY KEY (department_id),
    UNIQUE (department_name)
);

CREATE TABLE employee (
    employee_id         INTEGER,
    store_id            INTEGER,
    department_id       INTEGER,
    first_name          VARCHAR(50) NOT NULL,
    last_name           VARCHAR(50) NOT NULL,
    email_address       VARCHAR(100),
    phone_number        VARCHAR(20),
    hire_date           DATE,
    employment_status   VARCHAR(20),
    job_title           VARCHAR(50),
    hourly_rate         NUMERIC(10,2),
    annual_salary       NUMERIC(12,2),
    PRIMARY KEY (employee_id),
    UNIQUE (email_address),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (department_id)
        REFERENCES department (department_id)
        ON DELETE SET NULL,
    CHECK (employment_status IN ('Active', 'Inactive', 'On Leave', 'Terminated')),
    CHECK (hourly_rate IS NULL OR hourly_rate >= 0),
    CHECK (annual_salary IS NULL OR annual_salary >= 0)
);

CREATE TABLE product_category (
    category_id    INTEGER,
    category_name  VARCHAR(100) NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE customer (
    customer_id    INTEGER,
    first_name     VARCHAR(50) NOT NULL,
    last_name      VARCHAR(50) NOT NULL,
    phone_number   VARCHAR(20),
    email_address  VARCHAR(100),
    join_date      DATE,
    PRIMARY KEY (customer_id),
    UNIQUE (email_address)
);

CREATE TABLE vendor (
    vendor_id        INTEGER,
    vendor_name      VARCHAR(100) NOT NULL,
    contact_name     VARCHAR(100),
    phone_number     VARCHAR(20),
    email_address    VARCHAR(100),
    vendor_address   VARCHAR(200),
    vendor_status    VARCHAR(20),
    PRIMARY KEY (vendor_id),
    CHECK (vendor_status IN ('Active', 'Inactive', 'Suspended'))
);

CREATE TABLE store_department (
    store_id                INTEGER,
    department_id           INTEGER,
    department_manager_id   INTEGER,
    PRIMARY KEY (store_id, department_id),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id),
    FOREIGN KEY (department_id)
        REFERENCES department (department_id),
    FOREIGN KEY (department_manager_id)
        REFERENCES employee (employee_id)
);

CREATE TABLE product (
    product_id           INTEGER,
    category_id          INTEGER,
    product_name         VARCHAR(150) NOT NULL,
    brand_name           VARCHAR(100),
    package_size         VARCHAR(50),
    unit_of_measure      VARCHAR(30),
    barcode              VARCHAR(50),
    is_perishable        BOOLEAN,
    product_status       VARCHAR(20),
    current_unit_price   NUMERIC(10,2),
    PRIMARY KEY (product_id),
    UNIQUE (barcode),
    FOREIGN KEY (category_id)
        REFERENCES product_category (category_id)
        ON DELETE SET NULL,
    CHECK (current_unit_price IS NULL OR current_unit_price >= 0),
    CHECK (product_status IN ('Active', 'Inactive', 'Discontinued'))
);

CREATE TABLE customer_loyalty_account (
    loyalty_account_id  INTEGER,
    customer_id         INTEGER,
    points_balance      INTEGER DEFAULT 0,
    account_status      VARCHAR(20),
    created_at          TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (loyalty_account_id),
    UNIQUE (customer_id),
    FOREIGN KEY (customer_id)
        REFERENCES customer (customer_id)
        ON DELETE CASCADE,
    CHECK (points_balance >= 0),
    CHECK (account_status IN ('Active', 'Inactive', 'Suspended'))
);

ALTER TABLE store_department
ADD CONSTRAINT fk_store_department_store
    FOREIGN KEY (store_id)
    REFERENCES store (store_id)
    ON DELETE CASCADE;

ALTER TABLE store_department
ADD CONSTRAINT fk_store_department_department
    FOREIGN KEY (department_id)
    REFERENCES department (department_id)
    ON DELETE CASCADE;

ALTER TABLE store_department
ADD CONSTRAINT fk_store_department_manager
    FOREIGN KEY (department_manager_id)
    REFERENCES employee (employee_id)
    ON DELETE SET NULL;

CREATE TABLE vendor_product (
    vendor_id               INTEGER,
    product_id              INTEGER,
    vendor_product_code     VARCHAR(50),
    unit_cost               NUMERIC(10,2),
    lead_time_days          INTEGER,
    is_preferred_vendor     BOOLEAN,
    PRIMARY KEY (vendor_id, product_id),
    FOREIGN KEY (vendor_id)
        REFERENCES vendor (vendor_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE CASCADE,
    CHECK (unit_cost IS NULL OR unit_cost >= 0),
    CHECK (lead_time_days IS NULL OR lead_time_days >= 0)
);

CREATE TABLE inventory (
    inventory_id                INTEGER,
    store_id                    INTEGER,
    product_id                  INTEGER,
    quantity_on_hand            INTEGER,
    reorder_level               INTEGER,
    last_updated_at             TIMESTAMP WITHOUT TIME ZONE,
    aisle_code                  VARCHAR(20),
    aisle_location_description  VARCHAR(100),
    PRIMARY KEY (inventory_id),
    UNIQUE (store_id, product_id),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE CASCADE,
    CHECK (quantity_on_hand >= 0),
    CHECK (reorder_level >= 0)
);

CREATE TABLE purchase_order (
    purchase_order_id         INTEGER,
    store_id                  INTEGER,
    vendor_id                 INTEGER,
    created_by_employee_id    INTEGER,
    purchase_order_date       DATE,
    expected_delivery_date    DATE,
    purchase_order_status     VARCHAR(20),
    PRIMARY KEY (purchase_order_id),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (vendor_id)
        REFERENCES vendor (vendor_id)
        ON DELETE SET NULL,
    FOREIGN KEY (created_by_employee_id)
        REFERENCES employee (employee_id)
        ON DELETE SET NULL,
    CHECK (purchase_order_status IN ('Pending', 'Approved', 'Delivered', 'Cancelled')),
    CHECK (
        expected_delivery_date IS NULL
        OR purchase_order_date IS NULL
        OR expected_delivery_date >= purchase_order_date
    )
);

CREATE TABLE purchase_order_line (
    purchase_order_line_id  INTEGER,
    purchase_order_id       INTEGER,
    product_id              INTEGER,
    ordered_quantity        INTEGER,
    unit_cost_at_order      NUMERIC(10,2),
    received_quantity       INTEGER,
    PRIMARY KEY (purchase_order_line_id),
    FOREIGN KEY (purchase_order_id)
        REFERENCES purchase_order (purchase_order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE SET NULL,
    CHECK (ordered_quantity > 0),
    CHECK (unit_cost_at_order IS NULL OR unit_cost_at_order >= 0),
    CHECK (received_quantity IS NULL OR received_quantity >= 0),
    CHECK (
        received_quantity IS NULL
        OR ordered_quantity IS NULL
        OR received_quantity <= ordered_quantity
    )
);

CREATE TABLE delivery (
    delivery_id               INTEGER,
    purchase_order_id         INTEGER,
    vendor_id                 INTEGER,
    store_id                  INTEGER,
    received_by_employee_id   INTEGER,
    delivery_date             DATE,
    delivery_status           VARCHAR(20),
    delay_days                INTEGER,
    delay_reason              VARCHAR(255),
    PRIMARY KEY (delivery_id),
    FOREIGN KEY (purchase_order_id)
        REFERENCES purchase_order (purchase_order_id)
        ON DELETE SET NULL,
    FOREIGN KEY (vendor_id)
        REFERENCES vendor (vendor_id)
        ON DELETE SET NULL,
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (received_by_employee_id)
        REFERENCES employee (employee_id)
        ON DELETE SET NULL,
    CHECK (delivery_status IN ('Pending', 'Received', 'Delayed', 'Cancelled')),
    CHECK (delay_days IS NULL OR delay_days >= 0)
);

CREATE TABLE sales_transaction (
    sale_id            INTEGER,
    store_id           INTEGER,
    customer_id        INTEGER,
    employee_id        INTEGER,
    sale_timestamp     TIMESTAMP WITHOUT TIME ZONE,
    sales_subtotal     NUMERIC(12,2),
    discount_total     NUMERIC(12,2),
    tax_total          NUMERIC(12,2),
    total_amount       NUMERIC(12,2),
    points_earned      INTEGER,
    points_redeemed    INTEGER,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customer (customer_id)
        ON DELETE SET NULL,
    FOREIGN KEY (employee_id)
        REFERENCES employee (employee_id)
        ON DELETE SET NULL,
    CHECK (sales_subtotal IS NULL OR sales_subtotal >= 0),
    CHECK (discount_total IS NULL OR discount_total >= 0),
    CHECK (tax_total IS NULL OR tax_total >= 0),
    CHECK (total_amount IS NULL OR total_amount >= 0),
    CHECK (points_earned IS NULL OR points_earned >= 0),
    CHECK (points_redeemed IS NULL OR points_redeemed >= 0)
);

CREATE TABLE sales_transaction_line (
    sale_line_id      INTEGER,
    sale_id           INTEGER,
    product_id        INTEGER,
    quantity_sold     INTEGER,
    unit_price        NUMERIC(10,2),
    discount_amount   NUMERIC(10,2),
    line_total        NUMERIC(12,2),
    PRIMARY KEY (sale_line_id),
    FOREIGN KEY (sale_id)
        REFERENCES sales_transaction (sale_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE SET NULL,
    CHECK (quantity_sold > 0),
    CHECK (unit_price IS NULL OR unit_price >= 0),
    CHECK (discount_amount IS NULL OR discount_amount >= 0),
    CHECK (line_total IS NULL OR line_total >= 0)
);

CREATE TABLE payment (
    payment_id           INTEGER,
    sale_id              INTEGER,
    payment_method       VARCHAR(20),
    payment_amount       NUMERIC(12,2),
    payment_timestamp    TIMESTAMP WITHOUT TIME ZONE,
    confirmation_code    VARCHAR(100),
    PRIMARY KEY (payment_id),
    FOREIGN KEY (sale_id)
        REFERENCES sales_transaction (sale_id)
        ON DELETE CASCADE,
    CHECK (payment_method IN ('Cash', 'Credit Card', 'Debit Card', 'Mobile Payment', 'Gift Card')),
    CHECK (payment_amount IS NULL OR payment_amount >= 0)
);

CREATE TABLE accounting_record (
    accounting_record_id   INTEGER,
    store_id               INTEGER,
    sale_id                INTEGER,
    purchase_order_id      INTEGER,
    record_type            VARCHAR(20),
    record_category        VARCHAR(50),
    amount                 NUMERIC(12,2),
    record_date            DATE,
    description            VARCHAR(255),
    fiscal_period          VARCHAR(10),
    PRIMARY KEY (accounting_record_id),
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (sale_id)
        REFERENCES sales_transaction (sale_id)
        ON DELETE SET NULL,
    FOREIGN KEY (purchase_order_id)
        REFERENCES purchase_order (purchase_order_id)
        ON DELETE SET NULL,
    CHECK (amount IS NULL OR amount >= 0),
    CHECK (record_type IN ('Revenue', 'Expense', 'Adjustment'))
);

CREATE TABLE payroll_record (
    payroll_id          INTEGER,
    employee_id         INTEGER,
    store_id            INTEGER,
    period_start_date   DATE,
    period_end_date     DATE,
    pay_date            DATE,
    gross_pay           NUMERIC(12,2),
    deduction_amount    NUMERIC(12,2),
    net_pay             NUMERIC(12,2),
    hours_worked        NUMERIC(8,2),
    PRIMARY KEY (payroll_id),
    FOREIGN KEY (employee_id)
        REFERENCES employee (employee_id)
        ON DELETE SET NULL,
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    CHECK (gross_pay IS NULL OR gross_pay >= 0),
    CHECK (deduction_amount IS NULL OR deduction_amount >= 0),
    CHECK (net_pay IS NULL OR net_pay >= 0),
    CHECK (hours_worked IS NULL OR hours_worked >= 0),
    CHECK (
        period_end_date IS NULL
        OR period_start_date IS NULL
        OR period_end_date >= period_start_date
    ),
    CHECK (
        pay_date IS NULL
        OR period_end_date IS NULL
        OR pay_date >= period_end_date
    )
);

CREATE TABLE shift_schedule (
    shift_id           INTEGER,
    employee_id        INTEGER,
    store_id           INTEGER,
    department_id      INTEGER,
    shift_start_date   DATE,
    shift_end_date     DATE,
    clock_in_time      TIMESTAMP WITHOUT TIME ZONE,
    clock_out_time     TIMESTAMP WITHOUT TIME ZONE,
    shift_status       VARCHAR(20),
    PRIMARY KEY (shift_id),
    FOREIGN KEY (employee_id)
        REFERENCES employee (employee_id)
        ON DELETE SET NULL,
    FOREIGN KEY (store_id)
        REFERENCES store (store_id)
        ON DELETE SET NULL,
    FOREIGN KEY (department_id)
        REFERENCES department (department_id)
        ON DELETE SET NULL,
    CHECK (shift_status IN ('Scheduled', 'Completed', 'Missed', 'Cancelled')),
    CHECK (
        shift_end_date IS NULL
        OR shift_start_date IS NULL
        OR shift_end_date >= shift_start_date
    ),
    CHECK (
        clock_out_time IS NULL
        OR clock_in_time IS NULL
        OR clock_out_time >= clock_in_time
    )
);
