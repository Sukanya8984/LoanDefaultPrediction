document.getElementById("loanForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    document.getElementById("loader").style.display = "block";
    document.getElementById("result").innerHTML = "";

    const formData = {
        age: document.getElementById("age").value,
        income: document.getElementById("income").value,
        loanAmount: document.getElementById("loanAmount").value,
        creditScore: document.getElementById("creditScore").value,
        monthsEmployed: document.getElementById("monthsEmployed").value,
        interestRate: document.getElementById("interestRate").value,
        dtiRatio: document.getElementById("dtiRatio").value,
        loanTerm: document.getElementById("loanTerm").value,
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        document.getElementById("loader").style.display = "none";

        if (result.prediction === "Default") {
            document.getElementById("result").innerHTML = "<p style='color: red;'>You cannot apply for a loan.</p>";
        } else {
            document.getElementById("result").innerHTML = "<p style='color: green;'>You can apply for a loan.</p>";
        }

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("loader").style.display = "none";
        document.getElementById("result").innerHTML = "<p style='color: red;'>Error processing request.</p>";
    }
});

document.getElementById("refreshBtn").addEventListener("click", function() {
    location.reload();
});

document.getElementById("showInstructions").addEventListener("click", function() {
    const infoBox = document.getElementById("instructions");
    if (infoBox.style.display === "none") {
        infoBox.style.display = "block";
    } else {
        infoBox.style.display = "none";
    }
});
