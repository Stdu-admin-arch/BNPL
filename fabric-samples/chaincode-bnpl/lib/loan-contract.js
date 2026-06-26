'use strict';

const { Contract } = require('fabric-contract-api');

class LoanContract extends Contract {

    // Initialize the ledger with a test loan
    async initLedger(ctx) {
        const loans = [
            { id: 'LOAN001', customer: 'Alice', amount: 1000, balance: 1000, status: 'ACTIVE' },
        ];
        for (const loan of loans) {
            await ctx.stub.putState(loan.id, Buffer.from(JSON.stringify(loan)));
        }
    }

    // Create a new BNPL loan agreement
    async createLoan(ctx, id, customer, amount) {
        const loan = {
            id,
            customer,
            amount: parseInt(amount),
            balance: parseInt(amount),
            status: 'ACTIVE',
        };
        await ctx.stub.putState(id, Buffer.from(JSON.stringify(loan)));
        return JSON.stringify(loan);
    }

    // Make a payment against the loan
    async makePayment(ctx, id, amount) {
        const loanBytes = await ctx.stub.getState(id);
        if (!loanBytes || loanBytes.length === 0) throw new Error(`Loan ${id} does not exist`);
        
        let loan = JSON.parse(loanBytes.toString());
        loan.balance -= parseInt(amount);

        if (loan.balance <= 0) {
            loan.balance = 0;
            loan.status = 'PAID_IN_FULL';
        }

        await ctx.stub.putState(id, Buffer.from(JSON.stringify(loan)));
        return JSON.stringify(loan);
    }

    // Query a specific loan
    async queryLoan(ctx, id) {
        const loanBytes = await ctx.stub.getState(id);
        if (!loanBytes || loanBytes.length === 0) throw new Error(`Loan ${id} does not exist`);
        return loanBytes.toString();
    }
}

module.exports = LoanContract;
