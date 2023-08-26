import { onRequest } from "firebase-functions/v2/https";
import * as logger from "firebase-functions/logger";
import { setGlobalOptions } from "firebase-functions/v2";
import * as admin from "firebase-admin";

// Start writing functions
// https://firebase.google.com/docs/functions/typescript
// use functions V2, not V1.

setGlobalOptions({ region: "asia-southeast1" });

/**
 * sample function to get data. you'll need to create multiple APIs (one function = 1 API)
 * to CRUD the voteRequest collection.
 *
 * Basically, for security, frontend (the stuff in public directory) should not
 * directly call the database, even though firebase supports this with security
 * rules. Instead, have https-triggered functions (APIs) to
 * perform authentication before the necessary CRUD operations,
 * and let the frontend call these APIs. In this context, probably need to
 * validate the telegram user https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
 * then provide them the data.
 */
//
export const funcName = onRequest(async (req, res) => {
  logger.info("Hello logs!", { structuredData: true });
  const db = admin.firestore();
  const doc = await db.collection("users").doc("alovelace").get();
  res.send(doc.data());
});
