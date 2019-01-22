.PHONY: deploy

deploy:
	git push
	ssh dev "cd ~/proj/bot && git pull && systemctl restart bot && systemctl status bot"
