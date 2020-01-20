// React component of a form used to create/edit events. 
// It's part of a web application for the organisation LabVäst
// who I've been building a website for. 

import React from "react";
import { connect } from "react-redux"
import moment from "moment";
import DateTimePicker from "react-datetime-picker";
import { startGetEventImageUrl } from "../actions/events"


export class EventForm extends React.Component {
  constructor(props) {
    super(props);

    if (props.event) {
      this.state = {
        ...props.event, 
        image: undefined
      };
      this.state.createdAt = moment(props.event.createdAt).toDate();
      this.state.date = moment(props.event.date).toDate();

    } else {
      this.state = {
        id: "",
        uid: "",
        createdAt: new Date(),
        date: new Date(),
        title: "",
        message: "",
        location: "",
        cost: "", 
        registration: "",
        image: undefined,
        imageDownloadUrl: undefined,
        imageRef: "",
        type: ""
      };
    };
    this.state.minDate = new moment().startOf("day").toDate();
  };
 
  componentDidMount() {
    if (this.state.imageRef) {
      this.props.startGetEventImageUrl(this.state.imageRef).then((imageDownloadUrl) => {
        this.setState(() => ({ imageDownloadUrl }))
      });
    };
  };

  onTitleChange = (e) => {
    const title = e.target.value;
    this.setState(() => ({ title }));
  };

  onTypeChange = (e) => {
    const type = e.target.value;
    this.setState(() => ({ type }));
  };

  onDateChange = (date) => {
    if (date) {
      this.setState(() => ({ date }));
    };
  };

  onMessageChange = (e) => {
    const message = e.target.value;
    this.setState(() => ({ message }));
  };

  onLocationChange = (e) => {
    const location = e.target.value;
    this.setState(() => ({ location }));
  };

  onCostChange = (e) => {
    const cost = e.target.value;
    if (!cost || cost.match(/^\d{1,}$/)) {
      this.setState(() => ({ cost }));
    };
  };

  onRegistrationChange = (e) => {
    const registration = e.target.value;
    this.setState(() => ({ registration }));
  };

  onImageChange = (e) => {
    if (e.target.files[0]) {
      const image = e.target.files[0];
      this.setState(() => ({ image, imageDownloadUrl: URL.createObjectURL(image) }));
    } else {
      this.setState(() => ({ image: undefined, imageDownloadUrl: undefined }));
    };
  };

  inputsOk = () => {
    const errorMessageStart = "Var god ange";
    let errorMessage = errorMessageStart;
    
    if (!this.state.title) {
      errorMessage += " titel,";
    };
    if (!this.state.message) {
      errorMessage += " information,";
    };
    if (!this.state.location) {
      errorMessage += " plats,";
    };
    if (!this.state.type) {
      errorMessage += " eventtyp,";
    };
    if(!this.state.registration.match(/^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/) && this.state.registration !== "") {
      errorMessage += " giltig registreringslänk,";
    };

    if (errorMessage.length !== errorMessageStart.length) {
      this.setState(() => ({ error: errorMessage.substring(0, errorMessage.length - 1)}));
      return false;
    } else {
      this.setState(() => ({ error: "" }));
      return true;
    };
  };

  onSubmit = (e) => {
    e.preventDefault();
  
    if (this.inputsOk()) {
      let newEvent = {
        id: this.state.id,
        uid: this.state.uid,
        createdAt: moment(this.state.createdAt).valueOf(),
        date:  moment(this.state.date).valueOf(),
        title: this.state.title,
        message: this.state.message,
        location: this.state.location,
        cost: this.state.cost, 
        registration: this.state.registration,
        image: this.state.image,
        imageRef: this.state.imageRef,
        type: this.state.type
      };

      if (!newEvent.image) {
        delete newEvent.image;
      }

      this.props.onSubmit(newEvent);
    };
  };

  render() {
    return (
      <form onSubmit={this.onSubmit} className="form content-container">
        <h3>Titel</h3>
        <input 
        id="eventform_title_input"
        type="text"
        placeholder="Titel"
        autoFocus
        value={this.state.title}
        onChange={this.onTitleChange}
        />

        <h3>Eventtyp</h3>
        <select id="eventform_select" value={this.state.type} onChange={this.onTypeChange}>
          <option value={""}>Välj eventtyp</option>
          <option value="jakt">Jakt</option>
          <option value="utbildning">Utbildning</option>
          <option value="viltspår">Viltspår</option>
          <option value="utställning">Utställning</option>
          <option value="öppen träning">Öppen träning</option>
        </select>

        <h3>Datum</h3>
        <DateTimePicker 
          clearIcon={null}
          format={"dd/MM-y; hh:mm"}
          minDate={this.state.minDate}
          onChange={this.onDateChange}
          value={this.state.date}
        />

        <h3>Information</h3>
        <textarea 
          placeholder="Information om eventet"
          value={this.state.message}
          onChange={this.onMessageChange}
        />

        <h3>Plats</h3>
        <input 
        id="eventform_location_input"
        type="text"
        placeholder="Plats"
        value={this.state.location}
        onChange={this.onLocationChange}
        />

        <h3>Pris</h3>
        <input 
        id="eventform_cost_input"
        type="text"
        placeholder="Pris (kr)"
        value={this.state.cost}
        onChange={this.onCostChange}
        />

        <h3>Länk till registrering</h3>
        <input 
        id="eventform_registration_input"
        type="text"
        placeholder="Registreringslänk"
        value={this.state.registration}
        onChange={this.onRegistrationChange}
        />

        <h3>Bild</h3>
        <img src={this.state.imageDownloadUrl} />
        <input 
          accept="image/*"
          type="file"
          onChange={this.onImageChange}
        />        

        {this.state.error}
        <button>Spara event</button>
      </form>
    );
  };
};

const mapDispatchToProps = (dispatch) => ({
  startGetEventImageUrl: (imageRef) => dispatch(startGetEventImageUrl(imageRef))
});

export default connect(undefined, mapDispatchToProps)(EventForm);
