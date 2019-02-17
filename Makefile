.PHONY: deploy

deploy:
	git push
	ssh dev "cd ~/proj/bot && git pull && systemctl daemon-reload && systemctl restart bot && systemctl status bot"
