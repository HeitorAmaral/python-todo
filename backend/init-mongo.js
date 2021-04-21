db.createUser(
    {
        user: "mongouser",
        pwd: "MngDb321",
        roles:[
            {
                role: "readWrite",
                db: "todo"
            }
        ]
    }
);