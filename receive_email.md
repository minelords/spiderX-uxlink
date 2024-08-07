## Email receiving tutorial
>Referenced from [oiov](https://github.com/oiov/vmail)
 
**1.Register a [turso](https://turso.tech) account, create a database, and create an emails table**

After registration, you will be prompted to create a database. I named it `vmail` here,

![](https://img.inke.app/file/3773b481c78c9087140b1.png)

Select your database, you will see the "Edit Table" button, click and enter, continue to click the "SQL Runner" button in the upper left corner, and insert the [SQL Script](https://github.com/oiov/vmail/blob/main/packages/database/drizzle/0000_sturdy_arclight.sql) Copy to Terminal Run:

```bash
# Copy sql script to run on the terminal (packages/database/drizzle/0000_sturdy_arclight.sql)
CREATE TABLE `emails` (
 `id` text PRIMARY KEY NOT NULL,
 `message_from` text NOT NULL,
 `message_to` text NOT NULL,
 `headers` text NOT NULL,
 `from` text NOT NULL,
 `sender` text,
 `reply_to` text,
 `delivered_to` text,
 `return_path` text,
 `to` text,
 `cc` text,
 `bcc` text,
 `subject` text,
 `message_id` text NOT NULL,
 `in_reply_to` text,
 `references` text,
 `date` text,
 `html` text,
 `text` text,
 `created_at` integer NOT NULL,
 `updated_at` integer NOT NULL
);
```

**2.Deploy email workers**

```bash
git clone https://github.com/oiov/vmail

cd vmail

# Install dependencies
pnpm install
```

Fill in the necessary environment variables in `vmail/apps/email-worker/wrangler.toml` file.

- TURSO_DB_AUTH_TOKEN (turso table info from step 1，click `Generate Token`)
- TURSO_DB_URL (e.g. libsql://db-name.turso.io)
- EMAIL_DOMAIN (e.g. vmail.dev)

> If you don't do this step, you can add environment variables in the worker settings of Cloudflare

Then run cmds:

```bash
cd apps/email-worker

# Node environment required, and your need to install wrangler cli and login first, see https://developers.cloudflare.com/workers/wrangler/install-and-update
pnpm run deploy
```

**3.Configure email routing rules**

Set `Catch-all` action to Send to Worker

![](https://img.inke.app/file/fa39163411cd35fad0a7f.png)

**4.Next, you can log in to the Turso database to get the received verification code information**  

which can be obtained in batches using the Turso API

Done!
