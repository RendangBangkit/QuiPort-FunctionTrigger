import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("gcs-access.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def updateData(uid, fireDetected, accidentDetected, categories):
    docs = db.collection(u'reports').where(u'uid', u'==', uid).stream()
    for doc in docs:
        report_ref = db.collection(u'reports').document(f'{doc.id}')

        report_ref.update({
            u'ai_results.detected_class.fire': fireDetected,
            u'ai_results.detected_class.accident': accidentDetected,
            u'ai_results.categories': categories,
        })

