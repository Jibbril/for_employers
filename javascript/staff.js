// Script containing CRUD operations for staffmembers of a
// company website. Implements Firebase for database as well 
// as image storage. Implements Redux for local storage. 
// Manages both the operations for Firebase (method starts
// with "start") as well as Redux local store. 

import database, { storage } from "../firebase/firebase";
import uuid from "uuid";

export const createStaffMember = (staffMember) => ({
  type: "CREATE_STAFFMEMBER",
  staffMember
});

export const startCreateStaffMember = (staffMember) => {
  return (dispatch) => {
    if (staffMember.image) {
      const imageRef = "staff/" + uuid();

      return storage.ref().child(imageRef).put(staffMember.image).then(() => {
        delete staffMember.image;
        staffMember.imageRef = imageRef;
        return database.collection("staff").add(staffMember);
      }).then((docRef) => {
        dispatch(createStaffMember({
          ...staffMember,
          id: docRef.id
        }));
      });

    } else {
      return database.collection("staff").add(staffMember).then((docRef) => {
        dispatch(createStaffMember({
          ...staffMember,
          id: docRef.id
        }));
      });
    };
  };
};

export const setStaffMembers = (staffMembers) => ({
  type: "SET_STAFFMEMBERS",
  staffMembers
});

export const startSetStaffMembers = () => {
  return (dispatch) => {
    return database.collection("staff").get().then((querySnapshots) => {
      let staffMembers = querySnapshots.docs.map(doc => ({ ...doc.data(), id: doc.id }));
      staffMembers = staffMembers.sort((a,b) => {
        return a.sortingPriority > b.sortingPriority ? 1:-1
      });
      dispatch(setStaffMembers(staffMembers));
    });
  };
};

export const startGetStaffMemberImageUrl = (imageRef) => {
  return () => {
    return storage.ref().child(imageRef).getDownloadURL().then((downloadUrl) => {
      return downloadUrl;
    });
  };
};

export const editStaffMember  = (id, updates) => ({
  type: "EDIT_STAFFMEMBER",
  id,
  updates
});

export const startEditStaffMember = (id, updates) => {
  return (dispatch) => {
    if (updates.image) {
      return storage.ref(updates.imageRef).put(updates.image).then(() => {
        delete updates.image;
        return database.doc(`staff/${id}`).update(updates);
      }).then(() => {
        dispatch(editStaffMember(id, updates));
      });
    } else {
      return database.doc(`staff/${id}`).update(updates).then(() => {
        dispatch(editStaffMember(id, updates));
      });
    };
  };
};

export const removeStaffMember = ({ id }) => ({
  type: "REMOVE_STAFFMEMBER",
  id
});

export const startRemoveStaffMember = ({id, imageRef}) => {
  return (dispatch) => {
    if (imageRef) {
      return storage.ref(imageRef).delete().then(() => {
        return database.doc(`staff/${id}`).delete().then(() => {
          dispatch(removeStaffMember({ id }));
        });
      });
    } else {
      return database.doc(`staff/${id}`).delete().then(() => {
        dispatch(removeStaffMember({ id }));
      });
    };
  };
};

// Script containing CRUD operations for staffmembers of a
// company website. Implements Firebase for database as well 
// as image storage. Implements Redux for local storage. 
// Manages both the operations for Firebase (method starts
// with "start") as well as Redux local store. 