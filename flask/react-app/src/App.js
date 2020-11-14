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
import React, { useState } from 'react';
import IosRefresh from "react-ionicons/lib/IosRefresh"
import LogoGithub from "react-ionicons/lib/LogoGithub"

/*
IosCheckmarkCircle
MdCheckmarkCircle
IosRefresh
*/


function App() {
  let status = "working"

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


      <Container fluid style={{ backgroundColor: '#007bff' }}>
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
                  <Card.Text>
                    <IosRefresh style={{ width: '100%', margin: '0 auto' }} fontSize="60px" color="#347eff" rotate={true} />
                    <p style={{ textAlign: 'center' }}> {status} </p>
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
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div >
  );
}

export default App;
