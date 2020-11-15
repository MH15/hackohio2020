import logo from './logo.svg';
import './App.css';
import {
  Container,
  Row,
  Col,
  Navbar,
  Nav,
  NavDropdown,
  Form,
  FormControl,
  Button,
  Card,
  Modal

} from "react-bootstrap"
import React, { useState, useEffect } from 'react';
import IosRefresh from "react-ionicons/lib/IosRefresh"
import LogoGithub from "react-ionicons/lib/LogoGithub"
import MdPause from "react-ionicons/lib/MdPause"
import MdCheckmarkCircle from "react-ionicons/lib/MdCheckmarkCircle"
import IosCloseCircle from "react-ionicons/lib/IosCloseCircle"
import io from "socket.io-client";
const ENDPOINT = "localhost:3210";


/*
IosCheckmarkCircle
MdCheckmarkCircle
IosRefresh
*/




function App() {
  const [iconComponent, setIconComponent] = useState(<MdPause style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="#347eff" rotate={false} />)

  // let socket = io("127.0.0.1:3210")
  // socket.on("connect", (data) => {
  //   console.log(data);
  // })

  const [status, setStatus] = useState("inactive")
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8765');
    // Connection opened
    socket.addEventListener('open', function (event) {
      console.log("connected to server")
    });
    socket.addEventListener("message", data => {
      let json = JSON.parse(data.data)
      switch (json["type"]) {
        case "status":
          switch (json["value"]) {
            case "inactive":
              setIconComponent(<MdPause style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="#347eff" rotate={false} />)
              break
            case "working":
              setIconComponent(<IosRefresh style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="#347eff" rotate={true} />)
              break
            case "success":
              setIconComponent(<MdCheckmarkCircle style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="green" rotate={false} />)
              break
            case "failure":
              setIconComponent(<IosCloseCircle style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="red" rotate={false} />)
              break
          }
          setStatus(json["value"])
      }
      // setStatus(data);
      console.log(json);
    });
  }, []);

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);



  return (
    <div className="App">
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Face Mask Recognition</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          A project for <a href="https://hack.osu.edu/2020/">HackOH/IO 2020</a>.

        </Modal.Body>
        <Modal.Footer>
          <Button href="https://github.com/mh15/hackohio2020" variant="primary" onClick={handleClose} style={{ background: "hsl(210, 12.2%, 16.1%)", borderColor: "hsl(210, 12.2%, 16.1%)" }}>
            <LogoGithub color={"white"} />
          </Button>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>


      <Container fluid style={{
        backgroundColor: '#007bff',
        paddingBottom: '30px'
      }}>
        <Row>
          <Col>
            <Navbar bg="primary" expand="lg" text="light">
              <Navbar.Brand href="#home">Face Mask Recognition</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                  <Nav.Link onClick={handleShow}>About</Nav.Link>
                </Nav>
              </Navbar.Collapse>
            </Navbar>
          </Col>
        </Row>


        <Row>
          <Col>
            <Card bg={"dark"} text={"light"}>
              <Card.Header>Video Stream</Card.Header>
              <Card.Img variant="top" src="/video_feed" />
              <Card.Body>
                <Card.Title>Card Title</Card.Title>
                <Card.Text>
                  Some quick example text to build on the card title and make up the bulk of
                  the card's content.
    </Card.Text>
                <Button variant="primary">Go somewhere</Button>
              </Card.Body>
            </Card>
          </Col>


          <Col>
            <Row style={{ marginBottom: '20px' }}>
              <Card style={{ width: '100%' }} bg={"dark"} text={"light"}>
                <Card.Header>System Status</Card.Header>
                <Card.Body>
                  <Card.Text style={{ textAlign: 'center' }}>
                    {iconComponent}

                    {status}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Row>

            <Row>
              <Card bg={"dark"} text={"light"}>

                <Card.Header>Statistics</Card.Header>
                <Card.Body>
                  <Card.Text>
                    Some quick example text to build on the card title and make up the bulk of
                    the card's content.
    </Card.Text>
                </Card.Body>
              </Card>
            </Row>
          </Col>
        </Row>
      </Container>
    </div >
  );
}

export default App;
