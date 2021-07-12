
function randomheart() {
	var v = []
	choice = random(1)
	if (choice < .5){
		var angle = random(PI)
		a = tan(angle)
		if (angle < PI / 2) {
			v.push(2/(a*a+1))
			v.push(-(a*v[0]))
		}
		else{
			v.push(-2/(a*a+1))
			v.push(-(a*v[0]))
		}
	}
	else {
		v.push(random(-2,2))
		v.push(-acos(1-abs(v[0]))+PI)
	}
	return v
}

function Particle(x, y, exploder, hu){
	this.pos = createVector(x, y)
	this.exploder = exploder
	this.lifespan = 255
	this.hu = hu

	if (!this.exploder){
		this.vel = createVector(0, random(-14, -10))
	}
	else {
		v = randomheart()
		this.vel = createVector(v[0], v[1])
		this.vel.mult(4)
	}
	this.acc = createVector(0, 0)

	this.update_vel = function() {
		this.vel.mult(random(4)/4)
	}
	this.update = function(){
		if (this.exploder){
			this.vel.mult(0.9)
			this.lifespan -= 4
		}
		this.vel.add(this.acc)
		this.pos.add(this.vel)
		this.acc.mult(0)
	}

	this.applyForce = function(force){
		this.acc.add(force)
	}

	this.done = function() {
		if (this.lifespan < 0){
			return true
		}
		else {
			return false
		}
	}

	this.show = function(){
		colorMode(HSB)
		if (this.exploder){
			strokeWeight(2)
			stroke(hu,255,255, this.lifespan)
		}
		else {
			strokeWeight(4)
			stroke(hu,255,255)
		}
		point(this.pos.x, this.pos.y)
	}


}
