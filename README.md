# kalenderfilter

Load the configured calendar and split it up according to privacy setting of events.
There will be an all.ics (which is just a copy of the source calender) and a public.ics
containing only the events which are public.

The resulting files end up in a `www` subdirectory.

## Install
```
git clone https://github.com/Eigenbaukombinat/kalenderfilter.git
cd kalenderfilter
mkdir www
python3 -m venv py3
cp config.py.example config.py
```
Now edit config.py to your needs!

## Running

Use the provided update.sh to run this regularly via a cronjob or the like.
Make sure to change into your checkout directory before.

Example which runs every minute::

	* * * * * cd /path/to/your/kalenderfilter && ./update.sh
