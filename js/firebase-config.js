/* ═══════════════════════════════════════════
   Firebase – Real Firestore + Auth
   ═══════════════════════════════════════════ */

const firebaseConfig = {
    apiKey: "AIzaSyBWtjzd0NGiaCzmzrntQkQIe51OZlj8jFs",
    authDomain: "resqsync-4feea.firebaseapp.com",
    projectId: "resqsync-4feea",
    storageBucket: "resqsync-4feea.firebasestorage.app",
    messagingSenderId: "644169883094",
    appId: "1:644169883094:web:9461036e6ccc4cf937d877",
    measurementId: "G-KKD6Q95M63"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const auth = firebase.auth();

const FireDB = {
    // ── Save incident ──
    async saveIncident(incident) {
        try {
            incident.created_at = firebase.firestore.FieldValue.serverTimestamp();
            incident.created_at_iso = new Date().toISOString();
            await db.collection('incidents').doc(String(incident.id)).set(incident);
            console.log('✅ Saved to Firestore:', incident.id);
            return true;
        } catch (e) {
            console.warn('Firestore save error:', e.message);
            return false;
        }
    },

    // ── Get incidents ──
    async getIncidents(limit = 50) {
        try {
            const snap = await db.collection('incidents')
                .orderBy('created_at_iso', 'desc')
                .limit(limit)
                .get();
            if (snap.empty) return null;
            return snap.docs.map(d => ({ ...d.data(), _docId: d.id }));
        } catch (e) {
            console.warn('Firestore read error:', e.message);
            return null;
        }
    },

    // ── Update status ──
    async updateStatus(id, status) {
        try {
            await db.collection('incidents').doc(String(id)).update({
                status,
                updated_at: new Date().toISOString()
            });
            return true;
        } catch (e) {
            console.warn('Firestore update error:', e.message);
            return false;
        }
    },

    // ── Real-time listener ──
    onIncidents(callback) {
        return db.collection('incidents')
            .orderBy('created_at_iso', 'desc')
            .limit(20)
            .onSnapshot(snap => {
                const data = snap.docs.map(d => d.data());
                callback(data);
            }, err => console.warn('Listener error:', err.message));
    },

    // ── Save analytics event ──
    async logEvent(type, data) {
        try {
            await db.collection('analytics').add({
                type, data,
                timestamp: new Date().toISOString()
            });
        } catch (e) { /* silent */ }
    },

    // ── Auth: Anonymous sign-in for demo ──
    async signInAnonymous() {
        try {
            if (!auth.currentUser) {
                await auth.signInAnonymously();
                console.log('✅ Firebase Auth: Anonymous sign-in');
            }
        } catch (e) {
            console.warn('Auth error:', e.message);
        }
    }
};

// Auto sign-in
FireDB.signInAnonymous();
