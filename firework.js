function Firework() {

	this.hu = random(255)
	this.firework = new Particle(random(width), height, false, this.hu)
	this.exploded = false
	this.particles = []

	this.update = function() {
		if (!this.exploded){
			this.firework.applyForce(gravity)
			this.firework.update()

			if (this.firework.vel.y >= 0){
				this.exploded = true
				this.explode()
			}
		}

		else{
			for (var i = this.particles.length-1; i >= 0; i--){
				this.particles[i].applyForce(gravity)
				this.particles[i].update()

				if (this.particles[i].done()) {
					this.particles.splice(i, 1)
				}
			}
		}
	}

	this.explode = function () {
		for (var i = 0; i<300; i++)
		{
			this.particles.push(new Particle(this.firework.pos.x, this.firework.pos.y, true, this.hu))
			if (i > 100){
				this.particles[i].update_vel()
			}
		}
	}

	this.done = function() {
		if (this.exploded && this.particles.length === 0){
			return true
		}
		else {
			return false
		}
	}

	this.show = function() {
		if (!this.exploded){
			this.firework.show()
		}
		for (var i = 0; i < this.particles.length; i++){
			this.particles[i].show()
		}
	}
}